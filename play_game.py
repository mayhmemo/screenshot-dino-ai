import time
from PIL import Image
from mss import mss
import keyboard
import numpy as np
from keras.models import model_from_json

# Constants for screen resolution and frame size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FRAME_WIDTH = 160
FRAME_HEIGHT = 150

# Calculate the center of the screen
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

# Calculate the top-left corner of the frame
frame_left = center_x - (FRAME_WIDTH // 2)
frame_top = center_y - (FRAME_HEIGHT // 2)

# Define the frame dictionary
frame = {"top": frame_top, "left": frame_left, "width": FRAME_WIDTH, "height": FRAME_HEIGHT}

ss_manager = mss()  # We are using mss() for taking a screenshot
is_exit = False     # A variable for stopping the program

width = 80     # Width of all images
height = 75    # Height of all images

# A function for go down in the game
def down():
    keyboard.release("right")
    keyboard.release(keyboard.KEY_UP)
    keyboard.press(keyboard.KEY_DOWN)

# A function for go up in the game
def up():
    keyboard.release("right")
    keyboard.release(keyboard.KEY_DOWN)
    keyboard.press(keyboard.KEY_UP)

# A function for stopping the program
def exit():
    global is_exit
    is_exit = True

# MAIN PROGRAM
if __name__ == '__main__':
    keyboard.add_hotkey("esc", exit)    # If user clicks the 'esc', the program will stop

    # Load the model and weights
    model = model_from_json(open("model.json", "r").read())
    model.load_weights(".weights.h5")

    while True:
        if is_exit:
            keyboard.release(keyboard.KEY_DOWN)
            keyboard.release(keyboard.KEY_UP)
            break

        screenshot = ss_manager.grab(frame)
        image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        grey_image = image.convert("L")                       # Convert RGB image to grey_scale image
        a_img = np.array(grey_image.resize((width, height)))  # Resize the grey image and convert it to numpy array
        img = a_img / 255                                     # Normalize the image array

        X = np.array([img])                                   # Convert list X to numpy array
        X = X.reshape(X.shape[0], width, height, 1)           # Reshape the X
        prediction = model.predict(X)                         # Get prediction by using the model

        result = np.argmax(prediction)  # Convert one-hot prediction to the number
        print("--------------------------")

        if result == 0:   # go down
            down()
            print("down")
        elif result == 1:   # go up
            up()
            print("up")

        time.sleep(0.01)  # Adding a small delay to avoid excessive CPU usage

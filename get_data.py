import time
from PIL import Image
from mss import mss
import keyboard
import uuid
from pathlib import Path

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
count = 0           # A variable which count the screenshots
is_exit = False     # A variable for stopping the program

# A function for taking a screenshot
def take_screenshot(ss_id, key):
    global count
    count += 1
    print("{}: {}".format(key, count))
    img = ss_manager.grab(frame)
    image = Image.frombytes("RGB", img.size, img.rgb)
    image.save("./images/{}_{}_{}.png".format(key, ss_id, count))

# A function for stopping the program
def exit():
    global is_exit
    is_exit = True

# MAIN PROGRAM
if __name__ == '__main__':
    Path("./images/").mkdir(parents=True, exist_ok=True) # Create images directory if not exist
    keyboard.add_hotkey("esc", exit)    # If user clicks the 'esc', the program will stop
    ss_id = uuid.uuid4()                # An id for all screenshots

    while True: # An infinite loop for taking screenshot until user stops the program
        if is_exit == True:
            break

        try:
            if keyboard.is_pressed(keyboard.KEY_UP):        # If 'up' key is pressed
                take_screenshot(ss_id, "up")
                time.sleep(0.01)
            elif keyboard.is_pressed(keyboard.KEY_DOWN):    # If 'down' key is pressed
                take_screenshot(ss_id, "down")
                time.sleep(0.01)
            elif keyboard.is_pressed("right"):              # If 'right' key is pressed
                take_screenshot(ss_id, "right")
                time.sleep(0.01)
        except RuntimeError:
            continue

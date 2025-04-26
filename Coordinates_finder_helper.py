# Helper script to get mouse coordinates
import pyautogui
import time

print("Move your mouse to the top-left corner of the region and press Ctrl+C.")
try:
    while True:
        x, y = pyautogui.position()
        position_str = f"X: {str(x).rjust(4)} Y: {str(y).rjust(4)}"
        print(position_str, end='')
        print('\b' * len(position_str), end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nCoordinates captured.")

# Now you have the top-left (x, y). You'll need to estimate/measure the width and height.
# Repeat for each required region (question + 4 answers).
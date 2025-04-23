# -*- coding: utf-8 -*-

import pyautogui
import pytesseract
from PIL import Image, ImageGrab, ImageOps, ImageChops
import time
import random
import re
import imagehash  # for checking if images look different
import math 
import traceback  
import os  

# --- user needs to set these stuff ---
# path to tesseract exe, pls set this
try:
    pytesseract.get_tesseract_version()
    print("tesseract found yay")
except pytesseract.TesseractNotFoundError:
    tesseract_path = r''  # <-- pls put ur full path here!!
    if not tesseract_path: print("\noops no tesseract path..."); exit()
    try:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        pytesseract.get_tesseract_version()
        print(f"manual tesseract set to: {tesseract_path}")
    except Exception as e: print(f"\nerror with tesseract path prob: {tesseract_path}"); exit()
except Exception as e: print(f"something broke checking tesseract: {e}"); exit()

# screen areas to watch (left, top, width, height)
QUESTION_REGION = (880, 260, 300, 100)  # where question shows up
OPTIONS_REGIONS = [  # areas for answer choices
    (900, 370, 200, 50), 
    (900, 440, 200, 50),
    (900, 520, 200, 50),
    (900, 600, 200, 50),
]
BACK_TO_GAME_REGION = (900, 700, 200, 50)  # popup close button area

# behavior settings
MIN_DELAY_BEFORE_ACTION = 0.8; MAX_DELAY_BEFORE_ACTION = 2.5  # random wait before doing stuff
MIN_MOUSE_MOVE_DURATION = 0.2; MAX_MOUSE_MOVE_DURATION = 0.8  # how fast mouse moves
ERROR_RATE = 0  # chance to click wrong answer lol
MAX_ITERATIONS = 100000  # how many questions to try
RETRY_LIMIT = 5  # how many times to retry if stuck
ANIMATION_DELAY = 1.0  # wait for screen to update

# ocr settings
OCR_CONFIG = '--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789xX*'  # for questions
OCR_CONFIG_OPTIONS = '--psm 7 --oem 1 -c tessedit_char_whitelist=-0123456789.'  # for answers
OCR_CONFIG_POPUP = '--psm 7 --oem 1'  # for popups
POPUP_KEYWORDS = ["back", "game", "continue", "congrats"]  # words to look for in popups

# debug stuff
SAVE_DEBUG_IMAGES = False  # set true to save processed images
DEBUG_IMAGE_DIR = "ocr_debug_images"  # where to dump images
PREPROCESSING_THRESHOLD = 180  # image processing level

# some globals to track stuff
last_click_target_region = None
last_question_raw_text = None

def capture_screen_region(region, iteration_num=-1, region_name="unknown", save_debug=SAVE_DEBUG_IMAGES):
    """grabs screen area and processes it for ocr"""
    try:
        left, top, width, height = region
        if width <= 0 or height <= 0:
            print(f"weird region size for {region_name}, skipping")
            return None
        # take screenshot and make it bw
        screenshot = pyautogui.screenshot(region=region)
        img_processed = ImageOps.grayscale(screenshot)
        img_processed = img_processed.point(lambda p: 0 if p < PREPROCESSING_THRESHOLD else 255)
        img_processed = img_processed.convert('1')

        # save debug img if needed
        if save_debug and iteration_num != -1:
            if not os.path.exists(DEBUG_IMAGE_DIR):
                try: os.makedirs(DEBUG_IMAGE_DIR)
                except OSError as e: print(f"oops cant make debug dir: {e}")
            try:
                filename = os.path.join(DEBUG_IMAGE_DIR, f"iter_{iteration_num}_{region_name}.png")
                img_processed.save(filename)
            except Exception as save_err:
                print(f"couldnt save debug img: {save_err}")

        return img_processed
    except Exception as e:
        print(f"failed to capture {region_name}: {e}")
        return None

def ocr_image(image, config=OCR_CONFIG):
    """reads text from image using tesseract"""
    if image is None: return ""
    try:
        return pytesseract.image_to_string(image, config=config).strip()
    except Exception as e:
        print(f"ocr error lol: {e}")
        return ""

def clean_text_multiply(text):
    """tidies up multiplication questions"""
    if not text: return None
    text = text.lower().replace(' ','').replace('x', '*')
    cleaned = re.sub(r'[^\d\*]', '', text)
    if not re.fullmatch(r'\d+\*\d+', cleaned):
        return None
    return cleaned

def parse_and_solve_multiply(question_text_raw):
    """solves simple multiplication questions"""
    cleaned = clean_text_multiply(question_text_raw)
    if not cleaned: return None
    
    match = re.match(r'^(\d+)\*(\d+)$', cleaned)
    if not match: return None
    
    try:
        num1, num2 = map(int, match.groups())
        return num1 * num2
    except:
        return None

def clean_text_option(text):
    """cleans answer options text"""
    if not text: return None
    cleaned = re.sub(r'[^\-\d\.]', '', text)
    if not cleaned or cleaned in ['.', '-']: return None
    if cleaned.count('.') > 1:
        cleaned = cleaned[:cleaned.find('.')+1] + cleaned[cleaned.find('.')+1:].replace('.', '')
    if not re.fullmatch(r'-?\d+(\.\d+)?', cleaned):
        return None
    return cleaned

def get_random_point_in_region(region):
    """picks random spot in given area"""
    left, top, width, height = region
    return (
        random.randint(left, left + width - 1),
        random.randint(top, top + height - 1)
    )

def human_like_move_and_click(target_region, move_duration):
    """moves mouse and clicks like a human-ish"""
    global last_click_target_region
    try:
        x, y = get_random_point_in_region(target_region)
        pyautogui.moveTo(x, y, duration=move_duration, 
                        tween=random.choice([pyautogui.easeInQuad, pyautogui.easeOutQuad]))
        time.sleep(random.uniform(0.05, 0.15))
        pyautogui.click()
        last_click_target_region = target_region
    except Exception as e:
        print(f"whoops click error: {e}")

def compare_images(img1, img2):
    """checks if two images are different using hashing"""
    if img1 is None or img2 is None: return 999
    try:
        return imagehash.average_hash(img1) - imagehash.average_hash(img2)
    except Exception as e:
        print(f"cant compare images: {e}")
        return 999

def main():
    global last_click_target_region, last_question_raw_text
    print("starting...")
    print("make sure game window is visible!")
    for i in range(3, 0, -1):
        print(f"starting in {i}...")
        time.sleep(1)

    last_question_image = None
    retries = 0
    iterations = 0

    try:
        while iterations < MAX_ITERATIONS:
            current_iter = iterations + 1
            print(f"\n--- loop #{current_iter} ---")

            if iterations > 0:
                time.sleep(ANIMATION_DELAY)

            # grab question area
            question_img = capture_screen_region(QUESTION_REGION, current_iter, "q")
            if not question_img:
                print("no question img, waiting...")
                time.sleep(3)
                continue

            # read question text
            question_text = ocr_image(question_img, OCR_CONFIG)
            print(f"ocr got: '{question_text}'")

            # check if screen changed
            img_diff = compare_images(last_question_image, question_img)
            text_diff = question_text != last_question_raw_text if last_question_raw_text else True
            changed = img_diff >= 5 or text_diff

            if not changed and last_question_image:
                retries += 1
                if retries > RETRY_LIMIT:
                    print("prob stuck, checking for popup...")
                    for _ in range(10):
                        popup_img = capture_screen_region(BACK_TO_GAME_REGION, -1, "popup", False)
                        popup_text = ocr_image(popup_img, OCR_CONFIG_POPUP).lower()
                        if any(kw in popup_text for kw in POPUP_KEYWORDS):
                            print("found popup, clicking...")
                            human_like_move_and_click(BACK_TO_GAME_REGION, 0.3)
                            time.sleep(1.5)
                            break
                        time.sleep(0.5)
                    else:
                        print("no popup found, exiting")
                        break
                    retries = 0
                    continue
                else:
                    print(f"screen same, retry #{retries}")
                    if last_click_target_region:
                        human_like_move_and_click(last_click_target_region, 0.3)
                    time.sleep(1)
                    continue
            else:
                retries = 0
                last_question_image = question_img
                last_question_raw_text = question_text

            # solve question
            answer = parse_and_solve_multiply(question_text)
            if not answer:
                print("cant solve, clicking first option")
                if OPTIONS_REGIONS:
                    human_like_move_and_click(OPTIONS_REGIONS[0], 0.5)
                iterations += 1
                time.sleep(2)
                continue

            # read answer options
            options = []
            print("checking options...")
            for idx, region in enumerate(OPTIONS_REGIONS):
                opt_img = capture_screen_region(region, current_iter, f"opt{idx+1}")
                opt_text = clean_text_option(ocr_image(opt_img, OCR_CONFIG_OPTIONS))
                print(f"opt {idx+1}: {opt_text}")
                if opt_text: options.append({"text": opt_text, "region": region})

            # find matching answer
            target = None
            try:
                target_num = float(answer)
                closest = None
                min_diff = float('inf')
                for opt in options:
                    try:
                        opt_num = float(opt['text'])
                        diff = abs(opt_num - target_num)
                        if diff < 0.001:
                            target = opt['region']
                            break
                        if diff < min_diff:
                            closest = opt['region']
                            min_diff = diff
                    except: pass
                if not target and closest and min_diff < 0.1:
                    target = closest
            except: pass

            # decide where to click
            if not target:
                print("no good option, clicking first")
                target = OPTIONS_REGIONS[0]
            elif random.random() < ERROR_RATE:
                print("intentional wrong click!")
                wrongs = [r for r in OPTIONS_REGIONS if r != target]
                if wrongs: target = random.choice(wrongs)

            # do the click
            if target:
                human_like_move_and_click(target, random.uniform(0.2, 0.8))
                time.sleep(random.uniform(2, 3))

            iterations += 1

    except KeyboardInterrupt:
        print("\nstopped by user")
    except Exception as e:
        print(f"\nerror: {e}")
        traceback.print_exc()
    finally:
        print(f"\ndone, did {iterations} questions")

if __name__ == "__main__":
    main()
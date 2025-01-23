import keyboard
import time
import pyautogui
import requests
import io
import numpy as np
import cv2

image_url1 = "https://raw.githubusercontent.com/MustyxD/Gta/refs/heads/main/1920x1080kaz.png"
image_url2 = "https://raw.githubusercontent.com/MustyxD/Gta/refs/heads/main/2560x1440kaz.png"

def try_click(image_url):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image_bytes = io.BytesIO(response.content)
            image = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            if image is None:
                print(f"Error decoding image from {image_url}")
                return False
            location = pyautogui.locateCenterOnScreen(image, confidence=0.8, grayscale=True)
            if location:
                pyautogui.click(location)
                print(f"Clicked '{image_url}'")
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image from {image_url}: {e}")
            return False
        except cv2.error as e:
            print(f"Error decoding image: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
        
            
def anti():
    keyboard.press("w")
    keyboard.press("s")
    time.sleep(325)
    keyboard.release("w")
    keyboard.release("s")


def kaz():
    keyboard.send("up arrow")
    time.sleep(2)
    pyautogui.move(12, 12)
    time.sleep(10)

    if not try_click(image_url1):
        try_click(image_url2)

    time.sleep(10)
    keyboard.send("tab")
    keyboard.send("tab")
    keyboard.send("enter")
    time.sleep(10)
    keyboard.send("tab")
    keyboard.send("tab")
    keyboard.send("enter")
    time.sleep(10)
    keyboard.send("escape")
    keyboard.send("escape")
    keyboard.send("backspace")


def main():
    while True:
        
        time.sleep(10)
        anti()
        time.sleep(10)
        kaz()




if __name__ == "__main__":
    main()

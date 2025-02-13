import keyboard
import time
import pyautogui
import requests
import io
import numpy as np
import cv2
import threading
from mss import mss
from screeninfo import get_monitors
import os

# Константы
MATCH_THRESHOLD = 0.9
IMAGE_URLS = {
    "1920x1080": "https://raw.githubusercontent.com/MustyxD/Botik/refs/heads/main/1920x1080kaz.png",
    "2560x1440": "https://raw.githubusercontent.com/MustyxD/Botik/refs/heads/main/2560x1440kaz.png"
}
LOCAL_TEMPLATE_PATH = "template_kaz.png"

# Инициализация MSS для захвата экрана
sct = mss()

def get_primary_monitor():
    monitors = get_monitors()
    for monitor in monitors:
        if monitor.is_primary:
            return monitor
    return None

def download_image(image_url):
    """
    Загружает изображение по URL и возвращает его в формате OpenCV.
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        image_bytes = io.BytesIO(response.content)
        image = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Ошибка при декодировании изображения: {image_url}")
        return image
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

def capture_screen(monitor):
    """
    Захватывает область экрана.
    """     

    with mss() as sct:
        screenshot = np.array(sct.grab(monitor))[:, :, :3]  # Удаляем альфа-канал
    return cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

def is_template_present(image, template_path, threshold=MATCH_THRESHOLD):
    """
    Проверяет, присутствует ли шаблон на изображении.
    """
    try:
        # Загружаем шаблон
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            raise FileNotFoundError(f"Шаблон не найден: {template_path}")

        # Убедимся, что оба изображения имеют одинаковое количество каналов
        if len(image.shape) == 2:  # Если изображение одноканальное (градации серого)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Преобразуем в 3 канала (BGR)

        # Преобразуем изображение и шаблон в градации серого
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Выполняем поиск шаблона
        result = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Если максимальное значение превышает порог, считаем, что шаблон найден
        if max_val > threshold:
            return max_loc
        return None
    except Exception as e:
        print(f"Ошибка при поиске шаблона: {e}")
        return None

def try_click(image_url, monitor):
    """
    Пытается найти и кликнуть по шаблону, загруженному по URL.
    """
    try:
        # Загружаем изображение по URL
        template = download_image(image_url)
        if template is None:
            print(f"Не удалось загрузить шаблон: {image_url}")
            return False

        # Захватываем экран
        screen = capture_screen(monitor)

        # Выполняем поиск шаблона
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Если шаблон найден, кликаем по нему
        if max_val > MATCH_THRESHOLD:
            pyautogui.click(max_loc[0] + monitor["left"], max_loc[1] + monitor["top"])
            print(f"Кликнул по шаблону: {image_url}")
            return True

        print(f"Шаблон не найден: {image_url}")
        return False
    except Exception as e:
        print(f"Ошибка при попытке клика: {e}")
        return False
    
def anti():
    """
    Нажимает клавиши W и S на 5 секунд.
    """
    keyboard.press("w")
    keyboard.press("s")
    time.sleep(325)  
    keyboard.release("w")
    keyboard.release("s")

def kaz():
    """
    Выполняет действия для обработки шаблонов.
    """
    # Получаем главный монитор
    primary_monitor = get_primary_monitor()
    if primary_monitor is None:
        print("Главный монитор не найден!")
        return

    # Настройка области скриншота относительно центра главного монитора
    monitor = {
        "top": primary_monitor.y + primary_monitor.height // 2 - 800,
        "left": primary_monitor.x + primary_monitor.width // 2 - 100,
        "width": 1400,
        "height": 1600
    }

    # Захватываем экран
    screen = capture_screen(monitor)

    # Проверяем наличие локального шаблона
    if is_template_present(screen, LOCAL_TEMPLATE_PATH):
        keyboard.send("up arrow")
        time.sleep(5)
        pyautogui.move(50, 50)
        time.sleep(10)
        
        if not try_click(IMAGE_URLS["1920x1080"], monitor):
            try_click(IMAGE_URLS["2560x1440"], monitor)
            
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
    """
    Основной цикл программы.
    """
    while True:
        # Запускаем функцию kaz в отдельном потоке
        w_thread = threading.Thread(target=kaz, daemon=True)
        w_thread.start()

        # Выполняем функцию anti
        anti()

        # Ждём перед следующей итерацией
        time.sleep(10)

if __name__ == "__main__":
    main()
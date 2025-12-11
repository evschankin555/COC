#!/usr/bin/env python3
"""Автокликер для игры - автоматически кликает по кнопке "Надеть" в правой части экрана"""

import pyautogui
import time
import os
from pathlib import Path

# Настройки
BUTTON_IMAGE_PATH = "btn.png"  # Путь к изображению первой кнопки
BUTTON2_IMAGE_PATH = "btn2.png"  # Путь к изображению второй кнопки
CHECK_INTERVAL = 0.1  # Интервал проверки в секундах (0.1 = 100мс, очень быстро)
CONFIDENCE = 0.8  # Точность поиска (0.8 = 80%, можно снизить до 0.7 если не находит)
CLICK_DELAY = 0.01  # Минимальная задержка после клика для мгновенного возврата
DOUBLE_CLICK_DELAY = 1.0  # Задержка между кликами для второй кнопки (1 секунда)

# Безопасность: отключить fail-safe (чтобы не было проблем при движении мыши)
pyautogui.FAILSAFE = False

# Автоматическое определение области поиска (правая половина экрана)
def get_search_region():
    """Определяет правую половину экрана для поиска кнопки"""
    screen_width, screen_height = pyautogui.size()
    # Правая половина экрана: (x, y, width, height)
    region = (screen_width // 2, 0, screen_width // 2, screen_height)
    return region

def find_and_click_button(button_image_path: str, confidence: float = 0.8, region: tuple = None):
    """
    Ищет кнопку на экране (в указанной области) и кликает по ней
    
    Args:
        button_image_path: Путь к изображению кнопки
        confidence: Точность поиска (0.0-1.0)
        region: Область поиска (x, y, width, height) или None для всего экрана
    
    Returns:
        tuple: (найдено: bool, координаты: tuple или None)
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(button_image_path):
            print(f"[!] Файл изображения не найден: {button_image_path}")
            return False, None
        
        # Ищем кнопку на экране (только в указанной области)
        location = pyautogui.locateOnScreen(
            button_image_path,
            confidence=confidence,
            region=region,  # Ограничиваем поиск правой половиной экрана
            grayscale=False  # Можно включить grayscale=True для ускорения
        )
        
        if location:
            # Находим центр кнопки
            center = pyautogui.center(location)
            x, y = center
            
            print(f"[OK] Кнопка найдена! Координаты: ({x}, {y})")
            
            # Сохраняем текущую позицию курсора
            original_pos = pyautogui.position()
            
            # Мгновенный клик по кнопке
            pyautogui.click(x, y)
            time.sleep(CLICK_DELAY)
            
            # Возвращаем курсор точно на исходное место
            pyautogui.moveTo(original_pos.x, original_pos.y)
            
            print(f"[CLICK] Клик выполнен, курсор возвращен на ({original_pos.x}, {original_pos.y})")
            return True, (x, y)
        else:
            return False, None
    
    except pyautogui.ImageNotFoundException:
        return False, None
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        return False, None

def find_and_double_click_button(button_image_path: str, confidence: float = 0.8, region: tuple = None):
    """
    Ищет кнопку на экране (в указанной области) и выполняет двойной клик с задержкой
    
    Поведение: клик, пауза 1 секунда, еще один клик на том же месте
    
    Args:
        button_image_path: Путь к изображению кнопки
        confidence: Точность поиска (0.0-1.0)
        region: Область поиска (x, y, width, height) или None для всего экрана
    
    Returns:
        tuple: (найдено: bool, координаты: tuple или None)
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(button_image_path):
            print(f"[!] Файл изображения не найден: {button_image_path}")
            return False, None
        
        # Ищем кнопку на экране (только в указанной области)
        location = pyautogui.locateOnScreen(
            button_image_path,
            confidence=confidence,
            region=region,  # Ограничиваем поиск правой половиной экрана
            grayscale=False  # Можно включить grayscale=True для ускорения
        )
        
        if location:
            # Находим центр кнопки
            center = pyautogui.center(location)
            x, y = center
            
            print(f"[OK] Кнопка 2 найдена! Координаты: ({x}, {y})")
            
            # Сохраняем текущую позицию курсора
            original_pos = pyautogui.position()
            
            # Первый клик по кнопке
            pyautogui.click(x, y)
            print(f"[CLICK] Первый клик выполнен на ({x}, {y})")
            
            # Ждем 1 секунду
            time.sleep(DOUBLE_CLICK_DELAY)
            
            # Второй клик на том же месте
            pyautogui.click(x, y)
            time.sleep(CLICK_DELAY)
            
            # Возвращаем курсор точно на исходное место
            pyautogui.moveTo(original_pos.x, original_pos.y)
            
            print(f"[CLICK] Второй клик выполнен на ({x}, {y}), курсор возвращен на ({original_pos.x}, {original_pos.y})")
            return True, (x, y)
        else:
            return False, None
    
    except pyautogui.ImageNotFoundException:
        return False, None
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        return False, None

def main():
    """Основной цикл автокликера"""
    print("[START] Автокликер запущен!")
    print(f"[INFO] Ищу кнопку 1: {BUTTON_IMAGE_PATH}")
    print(f"[INFO] Ищу кнопку 2: {BUTTON2_IMAGE_PATH}")
    print(f"[INFO] Интервал проверки: {CHECK_INTERVAL} сек")
    print(f"[INFO] Точность поиска: {CONFIDENCE * 100}%")
    
    # Определяем область поиска (правая половина экрана)
    search_region = get_search_region()
    screen_width, screen_height = pyautogui.size()
    print(f"[INFO] Область поиска: правая половина экрана ({screen_width // 2}x{screen_height})")
    print("\n[INFO] Нажмите Ctrl+C для остановки\n")
    
    click_count_1 = 0  # Счетчик кликов для первой кнопки
    click_count_2 = 0  # Счетчик кликов для второй кнопки
    
    try:
        while True:
            # Проверяем первую кнопку (обычный клик)
            found_1, coords_1 = find_and_click_button(
                BUTTON_IMAGE_PATH, 
                CONFIDENCE, 
                region=search_region  # Поиск только в правой половине экрана
            )
            
            if found_1:
                click_count_1 += 1
                print(f"[STATS] Кнопка 1 - всего кликов: {click_count_1}\n")
            
            # Проверяем вторую кнопку (двойной клик с задержкой)
            found_2, coords_2 = find_and_double_click_button(
                BUTTON2_IMAGE_PATH, 
                CONFIDENCE, 
                region=search_region  # Поиск только в правой половине экрана
            )
            
            if found_2:
                click_count_2 += 1
                print(f"[STATS] Кнопка 2 - всего двойных кликов: {click_count_2}\n")
            
            # Небольшая задержка перед следующей проверкой
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print(f"\n\n[STOP] Автокликер остановлен")
        print(f"[STATS] Кнопка 1 - всего выполнено кликов: {click_count_1}")
        print(f"[STATS] Кнопка 2 - всего выполнено двойных кликов: {click_count_2}")

if __name__ == "__main__":
    main()


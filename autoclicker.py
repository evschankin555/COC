#!/usr/bin/env python3
"""Автокликер для игры - автоматически кликает по кнопке "Надеть" в правой части экрана"""

import pyautogui
import time
import os
from pathlib import Path

# Настройки
BUTTON_IMAGE_PATH = "btn.png"  # Путь к изображению первой кнопки
BUTTON2_IMAGE_PATH = "btn2.png"  # Путь к изображению второй кнопки
BUTTON3_IMAGE_PATH = "btn3.png"  # Триггер (картинка 3)
BUTTON4_IMAGE_PATH = "btn4.png"  # Цель (картинка 4) — нажать, когда виден триггер
BUTTON5_IMAGE_PATH = "btn5.png"  # Картинка 5 — кликнуть по ней при появлении
BUTTON5_ALT_IMAGE_PATH = "bt5.2.png"  # Вариация картинки 5 — тоже считать "кнопкой 5"
BUTTON6_IMAGE_PATH = "btn6.png"  # Картинка 6 — кликнуть по ней при появлении
BUTTON7_IMAGE_PATH = "btn7.png"  # Триггер 7 (по всему экрану)
BUTTON8_IMAGE_PATH = "btn8.png"  # Цель 8 — нажать, когда виден триггер 7 (по всему экрану)
BUTTON9_IMAGE_PATH = "btn9.png"  # Триггер 9
BUTTON10_IMAGE_PATH = "btn10.png"  # Шаг 1 (по триггеру 9)
BUTTON11_IMAGE_PATH = "btn11.png"  # Шаг 2 (по триггеру 9)
BUTTON12_IMAGE_PATH = "btn12.png"  # Шаг 3 (по триггеру 9)
BUTTON13_IMAGE_PATH = "btn13.png"  # Картинка 13 — кликнуть, но не чаще 1 раза в 30 сек
CHECK_INTERVAL = 0.1  # Интервал проверки в секундах (0.1 = 100мс, очень быстро)
CONFIDENCE = 0.8  # Точность поиска (0.8 = 80%, можно снизить до 0.7 если не находит)
CLICK_DELAY = 0.01  # Минимальная задержка после клика для мгновенного возврата
DOUBLE_CLICK_DELAY = 1.0  # Задержка между кликами для второй кнопки (1 секунда)
SEQ_CLICK_DELAY = 0.5  # Задержка между шагами в последовательности (0.5 сек)
BTN13_MIN_INTERVAL = 30.0  # минимальный интервал между кликами по btn13 (в секундах)

# Отдельные настройки распознавания для проблемных шаблонов
BTN5_CONFIDENCE = 0.65
BTN5_GRAYSCALE = True
BTN5_FALLBACK_FULL_SCREEN = True

# Безопасность: отключить fail-safe (чтобы не было проблем при движении мыши)
pyautogui.FAILSAFE = False

# Автоматическое определение области поиска (правая половина экрана)
def get_search_region():
    """Определяет правую половину экрана для поиска кнопки"""
    screen_width, screen_height = pyautogui.size()
    # Правая половина экрана: (x, y, width, height)
    region = (screen_width // 2, 0, screen_width // 2, screen_height)
    return region

def find_and_click_button(
    button_image_path: str,
    confidence: float = 0.8,
    region: tuple = None,
    grayscale: bool = False,
):
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
            grayscale=grayscale  # grayscale=True иногда лучше ловит мелкие/шумные иконки
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

def is_image_visible(
    image_path: str,
    confidence: float = 0.8,
    region: tuple = None,
    grayscale: bool = False,
) -> bool:
    """Проверяет, видна ли картинка на экране (в указанной области)."""
    try:
        if not os.path.exists(image_path):
            print(f"[!] Файл изображения не найден: {image_path}")
            return False

        location = pyautogui.locateOnScreen(
            image_path,
            confidence=confidence,
            region=region,
            grayscale=grayscale,
        )
        return location is not None
    except pyautogui.ImageNotFoundException:
        return False
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        return False

def click_target_image(
    target_image_path: str,
    confidence: float = 0.8,
    region: tuple = None,
    grayscale: bool = False,
):
    """Ищет target-картинку и кликает по ней 1 раз, с возвратом курсора."""
    return find_and_click_button(
        target_image_path,
        confidence=confidence,
        region=region,
        grayscale=grayscale,
    )

def click_any_target_image(
    target_image_paths: list[str],
    confidence: float = 0.8,
    region: tuple = None,
    grayscale: bool = False,
):
    """Пробует кликнуть по первой найденной картинке из списка."""
    for p in target_image_paths:
        found, coords = click_target_image(p, confidence=confidence, region=region, grayscale=grayscale)
        if found:
            return True, coords, p
    return False, None, None

def is_any_image_visible(
    image_paths: list[str],
    confidence: float = 0.8,
    region: tuple = None,
    grayscale: bool = False,
) -> bool:
    """True, если любая из картинок видна."""
    for p in image_paths:
        if is_image_visible(p, confidence=confidence, region=region, grayscale=grayscale):
            return True
    return False

def run_btn9_sequence(confidence: float, region: tuple):
    """
    Последовательность по триггеру btn9:
    - кликнуть по btn10
    - через 0.5 сек кликнуть по btn11
    - через 0.5 сек кликнуть по btn12
    """
    print("[INFO] Триггер 9 появился -> запускаю последовательность 10 -> 11 -> 12")

    found_10, _ = click_target_image(BUTTON10_IMAGE_PATH, confidence=confidence, region=region)
    if not found_10:
        print("[INFO] Шаг 1: btn10 не найден")
        return False

    time.sleep(SEQ_CLICK_DELAY)

    found_11, _ = click_target_image(BUTTON11_IMAGE_PATH, confidence=confidence, region=region)
    if not found_11:
        print("[INFO] Шаг 2: btn11 не найден")
        return False

    time.sleep(SEQ_CLICK_DELAY)

    found_12, _ = click_target_image(BUTTON12_IMAGE_PATH, confidence=confidence, region=region)
    if not found_12:
        print("[INFO] Шаг 3: btn12 не найден")
        return False

    print("[INFO] Последовательность 10 -> 11 -> 12 выполнена")
    return True

def main():
    """Основной цикл автокликера"""
    print("[START] Автокликер запущен!")
    print(f"[INFO] Ищу кнопку 1: {BUTTON_IMAGE_PATH}")
    print(f"[INFO] Ищу кнопку 2: {BUTTON2_IMAGE_PATH}")
    print(f"[INFO] Триггер 3: {BUTTON3_IMAGE_PATH} -> нажать: {BUTTON4_IMAGE_PATH}")
    print(f"[INFO] Кнопка 5: {BUTTON5_IMAGE_PATH} (клик по появлению)")
    print(f"[INFO] Кнопка 6: {BUTTON6_IMAGE_PATH} (клик по появлению)")
    print(f"[INFO] Триггер 7 (весь экран): {BUTTON7_IMAGE_PATH} -> нажать: {BUTTON8_IMAGE_PATH}")
    print(f"[INFO] Триггер 9: {BUTTON9_IMAGE_PATH} -> {BUTTON10_IMAGE_PATH} -> {BUTTON11_IMAGE_PATH} -> {BUTTON12_IMAGE_PATH}")
    print(f"[INFO] Кнопка 13: {BUTTON13_IMAGE_PATH} (не чаще 1 раза в {BTN13_MIN_INTERVAL} сек)")
    print(f"[INFO] Интервал проверки: {CHECK_INTERVAL} сек")
    print(f"[INFO] Точность поиска: {CONFIDENCE * 100}%")
    
    # Определяем область поиска (правая половина экрана)
    search_region = get_search_region()
    screen_width, screen_height = pyautogui.size()
    print(f"[INFO] Область поиска: правая половина экрана ({screen_width // 2}x{screen_height})")
    print("\n[INFO] Нажмите Ctrl+C для остановки\n")
    
    click_count_1 = 0  # Счетчик кликов для первой кнопки
    click_count_2 = 0  # Счетчик кликов для второй кнопки
    click_count_4 = 0  # Счетчик кликов по картинке 4 (по триггеру 3)
    trigger3_prev_visible = False  # чтобы нажимать btn4 только по появлению btn3
    trigger5_prev_visible = False  # чтобы нажимать btn5 только по появлению
    trigger6_prev_visible = False  # чтобы нажимать btn6 только по появлению
    trigger7_prev_visible = False  # чтобы нажимать btn8 только по появлению btn7
    trigger9_prev_visible = False  # чтобы запускать последовательность только по появлению btn9
    click_count_5 = 0
    click_count_6 = 0
    click_count_8 = 0
    seq9_count = 0
    click_count_13 = 0
    btn13_last_click_ts = 0.0
    
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

            # Триггер: если появилась картинка 3 — нажать картинку 4 (один раз на появление)
            trigger3_visible = is_image_visible(
                BUTTON3_IMAGE_PATH,
                CONFIDENCE,
                region=search_region,
            )

            if trigger3_visible and not trigger3_prev_visible:
                print("[INFO] Триггер 3 появился -> пытаюсь нажать кнопку 4")
                found_4, _coords_4 = click_target_image(
                    BUTTON4_IMAGE_PATH,
                    CONFIDENCE,
                    region=search_region,
                )
                if found_4:
                    click_count_4 += 1
                    print(f"[STATS] Кнопка 4 - всего кликов: {click_count_4}\n")
                else:
                    print("[INFO] Кнопка 4 не найдена, хотя триггер 3 виден")

            trigger3_prev_visible = trigger3_visible

            # Кнопка 5: кликнуть по появлению.
            # Поддерживаем два шаблона (btn5.png и bt5.2.png).
            # Для них используем отдельные настройки (пониже confidence + grayscale),
            # и при необходимости делаем fallback-поиск по всему экрану.
            btn5_templates = [BUTTON5_IMAGE_PATH, BUTTON5_ALT_IMAGE_PATH]
            trigger5_visible = is_any_image_visible(
                btn5_templates,
                BTN5_CONFIDENCE,
                region=search_region,
                grayscale=BTN5_GRAYSCALE,
            )
            if (not trigger5_visible) and BTN5_FALLBACK_FULL_SCREEN:
                trigger5_visible = is_any_image_visible(
                    btn5_templates,
                    BTN5_CONFIDENCE,
                    region=None,
                    grayscale=BTN5_GRAYSCALE,
                )
            if trigger5_visible and not trigger5_prev_visible:
                print("[INFO] Кнопка 5 появилась -> кликаю по ней")
                found_5, _coords_5, matched = click_any_target_image(
                    btn5_templates,
                    BTN5_CONFIDENCE,
                    region=search_region,
                    grayscale=BTN5_GRAYSCALE,
                )
                if (not found_5) and BTN5_FALLBACK_FULL_SCREEN:
                    found_5, _coords_5, matched = click_any_target_image(
                        btn5_templates,
                        BTN5_CONFIDENCE,
                        region=None,
                        grayscale=BTN5_GRAYSCALE,
                    )
                if found_5:
                    click_count_5 += 1
                    print(f"[STATS] Кнопка 5 - всего кликов: {click_count_5} (шаблон: {matched})\n")
            trigger5_prev_visible = trigger5_visible

            # Кнопка 6: кликнуть по появлению (в правой части экрана)
            trigger6_visible = is_image_visible(
                BUTTON6_IMAGE_PATH,
                CONFIDENCE,
                region=search_region,
            )
            if trigger6_visible and not trigger6_prev_visible:
                print("[INFO] Кнопка 6 появилась -> кликаю по ней")
                found_6, _ = click_target_image(BUTTON6_IMAGE_PATH, CONFIDENCE, region=search_region)
                if found_6:
                    click_count_6 += 1
                    print(f"[STATS] Кнопка 6 - всего кликов: {click_count_6}\n")
            trigger6_prev_visible = trigger6_visible

            # Триггер 7: по всему экрану. Если появился btn7 -> нажать btn8 (один раз на появление)
            trigger7_visible = is_image_visible(
                BUTTON7_IMAGE_PATH,
                CONFIDENCE,
                region=None,  # весь экран
            )
            if trigger7_visible and not trigger7_prev_visible:
                print("[INFO] Триггер 7 появился (весь экран) -> пытаюсь нажать кнопку 8")
                found_8, _ = click_target_image(BUTTON8_IMAGE_PATH, CONFIDENCE, region=None)
                if found_8:
                    click_count_8 += 1
                    print(f"[STATS] Кнопка 8 - всего кликов (по триггеру 7): {click_count_8}\n")
                else:
                    print("[INFO] Кнопка 8 не найдена, хотя триггер 7 виден")
            trigger7_prev_visible = trigger7_visible

            # Триггер 9: если появился btn9 -> последовательность btn10 -> btn11 -> btn12 (в правой части экрана)
            trigger9_visible = is_image_visible(
                BUTTON9_IMAGE_PATH,
                CONFIDENCE,
                region=search_region,
            )
            if trigger9_visible and not trigger9_prev_visible:
                ok = run_btn9_sequence(CONFIDENCE, region=search_region)
                if ok:
                    seq9_count += 1
                    print(f"[STATS] Последовательность по триггеру 9 - выполнено раз: {seq9_count}\n")
            trigger9_prev_visible = trigger9_visible

            # Кнопка 13: если видна — кликнуть, но не чаще 1 раза в 30 сек
            btn13_visible = is_image_visible(
                BUTTON13_IMAGE_PATH,
                CONFIDENCE,
                region=search_region,
            )
            if btn13_visible:
                now_ts = time.time()
                if (now_ts - btn13_last_click_ts) >= BTN13_MIN_INTERVAL:
                    print("[INFO] Кнопка 13 видна -> кликаю (rate-limit 30 сек)")
                    found_13, _ = click_target_image(BUTTON13_IMAGE_PATH, CONFIDENCE, region=search_region)
                    if found_13:
                        btn13_last_click_ts = now_ts
                        click_count_13 += 1
                        print(f"[STATS] Кнопка 13 - всего кликов: {click_count_13}\n")
            
            # Небольшая задержка перед следующей проверкой
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print(f"\n\n[STOP] Автокликер остановлен")
        print(f"[STATS] Кнопка 1 - всего выполнено кликов: {click_count_1}")
        print(f"[STATS] Кнопка 2 - всего выполнено двойных кликов: {click_count_2}")
        print(f"[STATS] Кнопка 4 - всего кликов (по триггеру 3): {click_count_4}")
        print(f"[STATS] Кнопка 5 - всего кликов: {click_count_5}")
        print(f"[STATS] Кнопка 6 - всего кликов: {click_count_6}")
        print(f"[STATS] Кнопка 8 - всего кликов (по триггеру 7): {click_count_8}")
        print(f"[STATS] Последовательность по триггеру 9 - выполнено раз: {seq9_count}")
        print(f"[STATS] Кнопка 13 - всего кликов: {click_count_13}")

if __name__ == "__main__":
    main()


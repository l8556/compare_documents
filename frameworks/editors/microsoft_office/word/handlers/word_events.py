# -*- coding: utf-8 -*-
from os.path import join, dirname, realpath

import pyautogui as pg
from rich import print
from time import sleep

from frameworks.decorators import singleton

from frameworks.host_control import Window, FileUtils

from ....events import Events


@singleton
class WordEvents(Events):

    def __init__(self):
        self.warning_windows = FileUtils.read_json(join(dirname(realpath(__file__)), 'warning_window.json'))

    @property
    def window_class_names(self) -> list:
        return ['OpusApp', "#32770", 'bosa_sdm_msword', 'ThunderDFrame', 'NUIDialog', "MsoSplash"]

    def _warning_window(self, hwnd: int) -> bool:
        for warning_window in self.warning_windows.items():
            data = warning_window[1]
            if Window.get_window_info(hwnd, data['window_title'], data['window_text']):
                print(f"[red]\n{'-' * 90}\n|WARNING WINDOW| {data['message']}\n{'-' * 90}")
                _button_info = Window.get_window_info(hwnd, data['button_title'], data['button_name'])[0]
                Window.click_on_button(_button_info)
                return True
        return False

    def when_opening(self, class_name, windows_text, hwnd: int = None) -> bool:
        match [class_name, windows_text]:

            case ['#32770', 'Microsoft Word']:
                hwnd = Window.get_hwnd('#32770', 'Microsoft Word') if not hwnd else hwnd
                if self._warning_window(hwnd):
                    raise
                print(f"[bold red]\n{'-' * 90}\n|ERROR| an error has occurred while opening the file\n{'-' * 90}")
                Window.close(hwnd)
                return True

            case ['bosa_sdm_msword', 'Преобразование файла']:
                print(f"[red]\n{'-' * 90}\n|WARNING WINDOW| Word File conversion\n{'-' * 90}")
                Window.close(hwnd)

            case [_, 'Пароль']:
                print(f"[red]\n{'-' * 90}\n|WARNING WINDOW| Enter password\n{'-' * 90}")
                pg.press('tab')
                pg.press('enter')

        return False

    def when_closing(self, class_name, windows_text, hwnd: int = None) -> bool:
        match [class_name, windows_text]:

            case ["NUIDialog", "Microsoft Word"]:
                print(f"[red]\n{'-' * 90}\n|WARNING WINDOW|Save file\n{'-' * 90}")
                pg.press('right')
                pg.press('enter')

            case ["#32770", "Microsoft Word"]:
                print(f"operation aborted")
                pg.press('enter')

    @staticmethod
    def handler(class_name, windows_text, hwnd: int = None):
        match [class_name, windows_text]:

            case ['#32770', 'Microsoft Word'] | \
                 ['NUIDialog', 'Извещение системы безопасности Microsoft Word']:
                Window.close(hwnd)
                pg.press('left')
                pg.press('enter')

            case ['#32770', 'Microsoft Visual Basic for Applications'] | \
                 ['bosa_sdm_msword', 'Преобразование файла'] | \
                 ['NUIDialog', 'Microsoft Word']:
                Window.close(hwnd)
                pg.press('enter')

            case ['bosa_sdm_msword', 'Пароль']:
                pg.press('tab')
                pg.press('enter')

            case ['#32770', 'Удаление нескольких элементов']:
                print(class_name, windows_text)

            case ['#32770', 'Сохранить как']:
                Window.close(hwnd)

            case ['bosa_sdm_msword', 'Показать исправления']:
                sleep(2)
                pg.press('tab', presses=3)
                pg.press('enter')
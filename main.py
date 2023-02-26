import random
import threading
import time

import pynput
import win32gui

window_name = "Command Prompt"
start_stop_key = "Key.f6"
window_switch_delay = 0.5


class Main:
    def __init__(self):
        self.running = True

        self.phrases = []

        self.last_phrase = ""

        with open("phrases.txt") as phrases_file:
            for line in phrases_file:
                self.phrases.append(line.strip())

    def get_window_names(self):
        window_names = []

        def winEnumHandler(hwnd, ctx):
            if (win32gui.IsWindowVisible(hwnd)):
                window_names.append(win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(winEnumHandler, None)

        return [string for string in window_names if string != ""]

    def get_window_handles(self):
        window_handles = []

        def winEnumHandler(window_handle, ctx):
            if (win32gui.IsWindowVisible(window_handle) and win32gui.GetWindowText(window_handle) == window_name):
                window_handles.append(window_handle)

        win32gui.EnumWindows(winEnumHandler, None)

        return window_handles

    def random_phrase(self):
        if len(self.phrases) != 0:
            self.phrase_index = random.randint(0, len(self.phrases) - 1)
            phrase = self.phrases[self.phrase_index]

            if self.last_phrase.lower() == phrase.lower():
                if len(self.phrases) > 1:
                    if self.phrase_index == 0:

                        phrase = self.phrases[self.phrase_index + 1]
                    elif self.phrase_index == len(self.phrases) - 1:
                        phrase = self.phrases[self.phrase_index - 1]
                    else:
                        phrase = self.phrases[self.phrase_index + 1]

            random_number = random.randint(0, 2)

            if random_number == 0:
                phrase = phrase.lower()
            elif random_number == 1:
                phrase = phrase.upper()
            else:
                phrase = phrase.title()

            self.last_phrase = phrase

            return phrase

    def main_loop(self):
        while True:
            if self.running:
                for handle in self.get_window_handles():
                    if not self.running:
                        break

                    win32gui.SetForegroundWindow(handle)

                    pynput.keyboard.Controller().type(self.random_phrase())

                    time.sleep(window_switch_delay)

    def on_press(self, key):
        if str(key) == start_stop_key:
            self.running = not self.running


def keyboard_listener(main):
    with pynput.keyboard.Listener(on_press=lambda key: main.on_press(key)) as keyboard_listener:
        keyboard_listener.join()


def main():
    main = Main()

    keyboard_listener_thred = threading.Thread(
        target=keyboard_listener, args=(main,))
    keyboard_listener_thred.daemon = True
    keyboard_listener_thred.start()

    main_loop_thred = threading.Thread(target=main.main_loop)
    main_loop_thred.daemon = True
    main_loop_thred.start()

    if len(main.get_window_handles()) == 0:
        print("error: no handles found")
    else:
        input("say something to quit: -> ")


if __name__ == "__main__":
    main()

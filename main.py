import random
import threading
import time

import pynput
import win32gui

window_name = "Window_Name"
chat_key = "/"
stop_key = "Key.f8"
switch_window_delay = 0.8


class Main:
    def __init__(self):
        self.phrases = []
        self.last_phrase = ""

        self.running = True

        with open("phrases.txt") as phrases_file:
            for line in phrases_file:
                self.phrases.append(line.strip())

    def get_window_handles(self):
        window_handles = []

        def winEnumHandler(window_handle, ctx):
            if (win32gui.IsWindowVisible(window_handle) and win32gui.GetWindowText(window_handle) == window_name):
                window_handles.append(window_handle)

        win32gui.EnumWindows(winEnumHandler, None)

        return window_handles

    def random_phrase(self):
        if len(self.phrases) != 0:
            phrase_index = random.randint(0, len(self.phrases) - 1)
            phrase = self.phrases[phrase_index]

            if self.last_phrase.lower() == phrase.lower():
                if len(self.phrases) > 1:
                    if phrase_index == 0:
                        phrase = self.phrases[phrase_index + 1]
                    elif phrase_index == len(self.phrases) - 1:
                        phrase = self.phrases[phrase_index - 1]
                    else:
                        phrase = self.phrases[phrase_index + 1]

            random_number = random.randint(0, 2)

            if random_number == 0:
                phrase = phrase.lower()
            elif random_number == 1:
                phrase = phrase.upper()
            else:
                phrase = phrase.title()

        else:
            phrase = ""

        self.last_phrase = phrase

        return phrase

    def say(self, string):
        pynput.keyboard.Controller().tap(key=chat_key)
        time.sleep(0.05)
        pynput.keyboard.Controller().type(string)
        time.sleep(0.05)
        pynput.keyboard.Controller().tap(pynput.keyboard.Key.enter)

    def main_loop(self):
        while True:
            if len(self.get_window_handles()) == 0 or not self.running:
                break

            for handle in self.get_window_handles():
                if not self.running:
                    break

                win32gui.SetForegroundWindow(handle)
                self.say(self.random_phrase())
                time.sleep(switch_window_delay)

    def on_press(self, key):
        if str(key) == stop_key:
            self.running = False


def keyboard_listener(main):
    with pynput.keyboard.Listener(on_press=lambda key: main.on_press(key)) as keyboard_listener:
        keyboard_listener.join()


def main():
    main = Main()

    keyboard_listener_thred = threading.Thread(
        target=keyboard_listener, args=(main,))
    keyboard_listener_thred.daemon = True
    keyboard_listener_thred.start()

    main.main_loop()


if __name__ == "__main__":
    main()

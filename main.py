import random
import threading
import time

import pynput
import win32gui

window_name = "Roblox"
stop_key = "Key.f6"
switch_window_delay = 0.4


class Main:
    def __init__(self):
        self.phrases = []

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

    def send_input(self):
        pynput.keyboard.Controller().tap(key="/")
        time.sleep(0.05)
        pynput.keyboard.Controller().type(random.choice(self.phrases))
        time.sleep(0.05)
        pynput.keyboard.Controller().tap(pynput.keyboard.Key.enter)

    def main_loop(self):
        while True:
            if len(self.get_window_handles()) == 0:
                break

            for handle in self.get_window_handles():
                if not self.running:
                    break

                win32gui.SetForegroundWindow(handle)
                self.send_input(self.random_phrase())
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

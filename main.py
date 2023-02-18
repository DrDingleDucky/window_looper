import threading
import time

import win32api
import win32gui
from pynput import keyboard

window_name = "Command Prompt"
start_stop_key = "Key.f6"
window_switch_delay = 0.5


class Main:
    def __init__(self):
        self.running = True

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

    def main_loop(self):
        while True:
            if len(self.get_window_handles()) == 0:
                print("Error: No Handles Found")
                break

            if self.running:
                for handle in self.get_window_handles():
                    if not self.running:
                        break

                    win32gui.SetForegroundWindow(handle)

                    keyboard.Controller().type("python")
                    keyboard.Controller().tap(keyboard.Key.enter)
                    keyboard.Controller().type("quit()")
                    keyboard.Controller().tap(keyboard.Key.enter)

                    time.sleep(window_switch_delay)

    def on_press(self, key):
        if str(key) == start_stop_key:
            self.running = not self.running


def keyboard_listener(main):
    with keyboard.Listener(on_press=lambda key: main.on_press(key)) as keyboard_listener:
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

    while True:
        command = input("Type 'quit' to quit: -> ").lower()

        if command == "quit":
            print("Quitting...")
            break

        else:
            print(f"'{command}' is not recognized. Type 'quit' to quit.")


if __name__ == "__main__":
    main()

print("Done")

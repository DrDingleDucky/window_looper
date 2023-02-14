import random
import time

import pynput
import win32gui

window_name = "Roblox"
chat_key = "/"

phrases = []
endings = []

last_phrase = ""
last_ending = ""


with open("phrases.txt") as phrases_file:
    for line in phrases_file:
        phrases.append(line.strip())

with open("endings.txt") as endings_file:
    for line in endings_file:
        endings.append(line.strip())


def random_phrase():
    global last_phrase
    global last_ending

    if len(phrases) != 0:
        phrase_index = random.randint(0, len(phrases) - 1)
        phrase = phrases[phrase_index]

        if last_phrase.lower() == phrase.lower():
            if len(phrases) > 1:
                if phrase_index == 0:
                    phrase = phrases[phrase_index + 1]
                elif phrase_index == len(phrases) - 1:
                    phrase = phrases[phrase_index - 1]
                else:
                    phrase = phrases[phrase_index + 1]

        random_number = random.randint(0, 2)

        if random_number == 0:
            phrase = phrase.lower()
        elif random_number == 1:
            phrase = phrase.upper()
        else:
            phrase = phrase.title()

    else:
        phrase = ""

    if len(endings) != 0:
        ending_index = random.randint(0, len(endings) - 1)
        ending = endings[ending_index]

        if last_ending.lower() == ending.lower():
            if len(endings) > 1:
                if ending_index == 0:
                    ending = endings[ending_index + 1]
                elif ending_index == len(endings) - 1:
                    ending = endings[ending_index - 1]
                else:
                    ending = endings[ending_index + 1]

    else:
        ending = ""

    last_phrase = phrase
    last_ending = ending

    return f"{phrase} {ending}"


def say(string):
    pynput.keyboard.Controller().tap(key=chat_key)
    time.sleep(0.05)
    pynput.keyboard.Controller().type(string)
    time.sleep(0.05)
    pynput.keyboard.Controller().tap(pynput.keyboard.Key.enter)


# def get_window_names():
#     window_names = []

#     def winEnumHandler(hwnd, ctx):
#         if (win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == window_name):
#             window_names.append(win32gui.GetWindowText(hwnd))

#     win32gui.EnumWindows(winEnumHandler, None)

#     return window_names


def get_window_handles():
    window_handles = []

    def winEnumHandler(hwnd, ctx):
        if (win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == window_name):
            window_handles.append(hwnd)

    win32gui.EnumWindows(winEnumHandler, None)

    return window_handles


def main():
    while True:
        for handle in get_window_handles():
            win32gui.SetForegroundWindow(handle)
            say(random_phrase())
            time.sleep(0.8)


if __name__ == "__main__":
    main()

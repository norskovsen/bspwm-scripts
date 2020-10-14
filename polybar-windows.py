#!/usr/bin/python3
import listen
import os
import re
import titlehandler
import threading

COLOR1 = "ffffff"
UNFOCUSED_COLOR = "777777"
BG = "ee222222"
MAX_SHORT_LENGTH = 20
MAX_LENGTH = 50
ACTIVE_DECORATION = "%{O5}"
INACTIVE_DECORATION_LEFT = "%{O5}%{F#" + UNFOCUSED_COLOR + \
                           "}%{u#" + COLOR1 + "}"
INACTIVE_DECORATION_RIGHT = "%{-u}%{F-}%{O5}"

CURRENT_DISPLAY_CMD = 'wmctrl -d | grep "*"'
WINDOWS_CMD = 'wmctrl -lx'
ACTIVE_WINDOW_CMD = "xprop -root _NET_ACTIVE_WINDOW|cut -d ' ' -f 5|sed -e 's/../0&/2'"


def get_short_title(title):
    if len(title) > MAX_SHORT_LENGTH:
        return title[:MAX_SHORT_LENGTH] + "..."
    return title


def format_title(process_name, title):
    if 'Chrome' in title:
        return "".join(title.split('-')[:-1]).strip()

    if len(title) > MAX_LENGTH:
        return title[:MAX_LENGTH] + "..."

    return title


def print_current_windows(update):
    current_display = os.popen(CURRENT_DISPLAY_CMD).read().split()[0]
    active_window = os.popen(ACTIVE_WINDOW_CMD).read().strip()
    windows = os.popen(WINDOWS_CMD).read().strip().split("\n")
    output = []
    for window_info in windows:
        try:
            window, display, process_name, user, *title = window_info.split()
        except Exception:
            continue
        title = " ".join(title)

        title = format_title(process_name, title)

        if display != current_display:
            continue

        if window == active_window.strip():
            output.append(ACTIVE_DECORATION + title + ACTIVE_DECORATION)
            continue

        title = get_short_title(title)
        output.append(INACTIVE_DECORATION_LEFT + title + INACTIVE_DECORATION_RIGHT)

    if len(output) > 0:
        output = "".join(output)[5:]
    else:
        output = " "

    print(output, flush=True)


if __name__ == '__main__':
    print_current_windows("")

    title_thread = threading.Thread(target=titlehandler.setup_loop, 
                                    args=(print_current_windows,))
    title_thread.start()

    node_thread = threading.Thread(target=listen.setup_loop,
                                   args=('bspc subscribe node',
                                         print_current_windows))
    node_thread.start()
    try:
        title_thread.join()
        node_thread.join()
    except Exception:
        print("hi")
        pass
    # titlehandler.setup_loop(func=print_current_windows)

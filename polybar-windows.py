#!/usr/bin/python3
import listen
import os

COLOR1 = "ffffff"
UNFOCUSED_COLOR = "777777"
BG = "ee222222"
MAX_LENGTH = 20
ACTIVE_DECORATION = "%{O5}"
INACTIVE_DECORATION_LEFT = "%{O5}%{F#" + UNFOCUSED_COLOR + \
                           "}%{u#" + COLOR1 + "}"
INACTIVE_DECORATION_RIGHT = "%{-u}%{F-}%{O5}"

CURRENT_DISPLAY_CMD = 'wmctrl -d | grep "*"'
ACTIVE_WINDOW_CMD = "xprop -root _NET_ACTIVE_WINDOW|cut -d ' ' -f 5|sed -e 's/../0&/2'"


def get_short_title(title):
    if len(title) > MAX_LENGTH:
        return title[:MAX_LENGTH] + "..."
    return title


def format_title(title):
    if 'Chrome' in title:
        return title.split('-')[-1].strip()

    return title


def print_current_windows(update):
    current_display = os.popen(CURRENT_DISPLAY_CMD).read().split()[0]
    active_window = os.popen(ACTIVE_WINDOW_CMD).read().strip()
    windows = os.popen('wmctrl -lx').read().strip().split("\n")
    output = []
    for window_info in windows:
        window, display, process_name, user, *title = window_info.split()
        title = " ".join(title)

        title = format_title(title)

        if display != current_display:
            continue

        if window == active_window.strip():
            output.append(ACTIVE_DECORATION + title + ACTIVE_DECORATION)
            continue

        title = get_short_title(title)
        output.append(INACTIVE_DECORATION_LEFT + title + INACTIVE_DECORATION_RIGHT)

    print("".join(output)[5:], flush=True)


if __name__ == '__main__':
    print_current_windows("")
    listen.setup_loop(cmd='bspc subscribe node', func=print_current_windows)

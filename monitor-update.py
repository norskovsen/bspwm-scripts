#!/usr/bin/python3
import os
import time
import listen

INTERVAL = 2

last_update = time.time()


def update_monitor(update):
    global last_update
    current_time = time.time()
    if (last_update - current_time) <= INTERVAL:
        return
    last_update = current_time
    time.sleep(2)
    os.system('~/.config/autorandr/postswitch')


if __name__ == '__main__':
    update_monitor("")
    listen.setup_loop(cmd='bspc subscribe monitor', func=update_monitor)

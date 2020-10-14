#!/usr/bin/python3
import os
import time
import listen
import threading

INTERVAL = 4

last_update = 0


def call_script(sleep=True):
    if sleep:
        time.sleep(2)
    os.system('~/.config/autorandr/postswitch')


def update_monitor(update):
    global last_update
    current_time = time.time()
    if abs(last_update - current_time) <= INTERVAL:
        return
    last_update = current_time
    thread = threading.Thread(target=call_script, args=tuple())
    thread.run()


if __name__ == '__main__':
    call_script(sleep=False)
    listen.setup_loop(cmd='bspc subscribe monitor', func=update_monitor)

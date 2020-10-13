#!/usr/bin/python3
import os
import listen
import subprocess
import time


def sound_reset():
    print("Sound update")
    os.system('killall volumeicon')
    my_env = os.environ.copy()
    my_env["GTK_THEME"] = 'Arc:dark'
    subprocess.Popen(['volumeicon'], env=my_env)


def sound_update(update):
    update = update.decode("utf-8").strip()
    if "card" in update and ("remove" in update or "new" in update):
        sound_reset()


if __name__ == '__main__':
    sound_reset()
    listen.setup_loop(cmd='pactl subscribe', func=sound_update)


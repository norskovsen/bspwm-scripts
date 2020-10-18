#!/usr/bin/python3
from pynput.keyboard import Listener
import notify2
import os
import alsaaudio

BRIGHTNESS_UP = 269025026
BRIGHTNESS_DOWN = 269025027

VOLUME_UP = 269025043
VOLUME_DOWN = 269025041
VOLUME_MUTE = 269025042


def get_loading(procent):
    procent //= 5
    return "[" + ("=" * procent) + " " * (20 - procent) + "]"


def send_brightness_notification():
    brightness = int(float(os.popen('light').read()))
    n.update(f"Brightness ({brightness}%)")
    n.show()


def brightness_up():
    os.system('light -A 10')
    send_brightness_notification()


def brightness_down():
    os.system('light -U 10')
    send_brightness_notification()


def get_volume():
    return alsaaudio.Mixer().getvolume()[0]


def send_volume_notification():
    volume = get_volume()
    if is_muted():
        text = "Volume (MUTED)"
    else:
        text = f"Volume ({volume}%)"
    n.update(text)
    n.show()


def volume_up():
    if is_muted():
        volume_toggle_mute()

    alsaaudio.Mixer().setvolume(min(100, get_volume()+5))
    send_volume_notification()


def volume_down():
    if is_muted():
        volume_toggle_mute()

    alsaaudio.Mixer().setvolume(max(0, get_volume()-5))
    send_volume_notification()


def is_muted():
    return alsaaudio.Mixer().getmute()[0]


def volume_toggle_mute(internal=False):
    alsaaudio.Mixer().setmute(not is_muted())
    if not internal:
        send_volume_notification()

def on_press(key):
    if "vk" not in dir(key):
        return

    if key.vk == BRIGHTNESS_DOWN:
        brightness_down()
    elif key.vk == BRIGHTNESS_UP:
        brightness_up()
    elif key.vk == VOLUME_DOWN:
        volume_down()
    elif key.vk == VOLUME_UP:
        volume_up()
    elif key.vk == VOLUME_MUTE:
        volume_toggle_mute()


if __name__ == '__main__':
    notify2.init('my-control')
    n = notify2.Notification(None)
    n.set_timeout(4000)
    with Listener(on_press=on_press) as listener:
        listener.join()

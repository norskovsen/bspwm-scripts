import subprocess


def setup_loop(cmd, func):
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    while True:
        update = p.stdout.readline()
        func(update)

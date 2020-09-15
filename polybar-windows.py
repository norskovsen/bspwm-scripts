#!/usr/bin/python3
from time import sleep


def main():
    i = 0
    while True:
        print("Hello!!!" + str(i), flush=True)
        sleep(1)
        i += 1


if __name__ == '__main__':
    main()

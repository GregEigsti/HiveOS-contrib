#!/usr/bin/env python

import commands
import time

def twinkle(gpu=0, count=60, duration=1):
    """
    Turns a GPU's logo LEDs on and off count times with duration sleep between
        gpu      - number of gpu to work on, defaults to 0
        count    - number of times to toggle LED, defaults to 60
        duration - length of time to sleep between iterations, defaults to 1 (second)
    """
    # loop count times
    for i in range(count):
        # if loop count is evenly divisible by 2 prepare to turn on the LEDs
        if i % 2:
            brightness = 100
            print 'GPU LED ON'
        # otherwise prepare to turn off the LEDs
        else:
            brightness = 0
            print 'GPU LED OFF'

        # execute the command
        output = commands.getoutput('DISPLAY=:0 nvidia-settings -a [gpu:{}]/GPULogoBrightness={}'.format(gpu, brightness))
        print output

        """
        Example shell commands to get/stop/start GPUCurrentFanSpeed for GPU4

        The danger around shutting down fans should be obvious. Understand what you are doing
        and how to correct things before proceeding.

        Before starting/stopping fans make a visual inventory of each card's fan speed;
        some cards do not shut down fans all the way and will leave them spinning slowly.
        It is best to know what to look for quickly before executing these commands.

        Get current fan speed for GPU4
        DISPLAY=:0 nvidia-settings -q [fan:4]/GPUCurrentFanSpeed
        Set current fan speed for GPU4 to 0
        DISPLAY=:0 nvidia-settings -a [fan:4]/GPUTargetFanSpeed=0
        Set current fan speed for GPU4 back to something acceptable
        DISPLAY=:0 nvidia-settings -a [fan:4]/GPUTargetFanSpeed=90
        """

        # sleep duration seconds
        time.sleep(duration)


def main():
    # cycle through gpus 0-7
    for gpu in range(8):
        # turn gpu's lights on/off 10 times with a second between
        twinkle(gpu, 10, 1)

if __name__ == "__main__":
    main()

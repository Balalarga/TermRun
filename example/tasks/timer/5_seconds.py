""" 5 seconds timer
"""
import time

import invoke
from termrun import term_runnable


@term_runnable(title="start")
def start_timer(ctx: invoke.Context):
    seconds = 5
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r") # Overwrites the previous line of output
        time.sleep(1)
        seconds -= 1
    print("Time is up!")

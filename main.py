#!/usr/bin/env python3
from RandomizedVideoTimer import RandomizedVideoTimer
import sys, time

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("""usage: main.py [url] [lsl] [usl]
        
required arguments:
    [url] - url for requesting song
    [lsl] - minimum seconds for rando song stop
    [usl] - max seconds for random song stop""")
        
    else:
        r1 = RandomizedVideoTimer(*sys.argv[1:4], optional_addons=("ublock_origin-1.54.0.xpi"))
        r1.load_video()
        r1.video_randomization()
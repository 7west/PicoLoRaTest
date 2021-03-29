# main.py - sets up LoRa RFM95W and offers functions to run change configuration and run tests

from machine import SPI, Pin
from rfm import printBW,printCodingRates
import time, rfm

g0 = Pin(14, Pin.IN)

rfm.init()


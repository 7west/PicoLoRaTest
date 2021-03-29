# rfm.py - 

from machine import Pin
import spiX, time

_rst = Pin(15, Pin.OUT)
_bwDict = {7.8 : 0x0, 10.4 : 0x1, 15.6 : 0x2, 20.8 : 0x3, 31.25 : 0x4, 
            41.7 : 0x5, 62.5 : 0x6, 125 : 0x7, 250 : 0x8, 500 : 0x9}
_currentBW = 125
_codingRateDict = {5 : 0x1, 6 : 0x2, 7 : 0x3, 8 : 0x4}
_currentCodingRate = 5

def setBW(bw):
    global _currentBW
    _currentBW = bw
    setModemConfig1()

def setCodingRate(cr):
    global _currentCodingRate
    _currentCodingRate = cr
    setModemConfig1()
    
def setModemConfig1():
    global _currentCodingRate, _currentBW
    config = (_bwDict[_currentBW] << 4) | (_codingRateDict[_currentCodingRate] << 1) | 1
    spiX.writeSpi(0x1D, config)

def init():
    _rst.high()
    time.sleep(0.1)

    if spiX.readSpi(0x42) != 0x12:
        raise Exception("ERROR: RFM not detected")
    else:
        print("RFM95 detected")
    
    spiX.writeSpi(0x01,0x80)  # LoRa M
    time.sleep(0.01)
    if spiX.readSpi(0x01) != 0x80:
        raise Exception("Failed to set RFM to LoRa Mode")
    spiX.writeSpi(0x0E,0x00)  # sets rx and tx buffer pointers to 0
    spiX.writeSpi(0x0F,0x00)
    setModemConfig1()
    # other init stuff






# Miscellaneous Functions
def printBW():
    print("Available bandwidths:")
    for key in _bwDict.keys():
        print("  ", key, "kHz")

def printCodingRates():
    print("Available coding rates:")
    for key in _codingRateDict.keys():
        print("  4/",key)
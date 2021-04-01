# rfm.py - 

from machine import Pin
import spiX, time

_rst = Pin(15, Pin.OUT)
_bwDict = {7.8 : 0x0, 10.4 : 0x1, 15.6 : 0x2, 20.8 : 0x3, 31.25 : 0x4, 
            41.7 : 0x5, 62.5 : 0x6, 125 : 0x7, 250 : 0x8, 500 : 0x9}
_currentBW = 125
_codingRateDict = {5 : 0x1, 6 : 0x2, 7 : 0x3, 8 : 0x4}
_currentCodingRate = 5
_currentSF = 7
_currentPower = 17
_currentBP = False
M_STDBY = 0x01
M_SLEEP = 0x00
M_LORA = 0x80
M_TX = 0x03
M_RX = 0x05

def setBW(bw):
    global _currentBW
    _currentBW = bw
    setModemConfig1()

def setCodingRate(cr):
    global _currentCodingRate
    _currentCodingRate = cr
    setModemConfig1()

def setSF(sf):
    global _currentSF
    _currentSF = sf
    setModemConfig2()

def setModemConfig1():
    global _currentCodingRate, _currentBW
    config = (_bwDict[_currentBW] << 4) | (_codingRateDict[_currentCodingRate] << 1)
    spiX.write(0x1D, config)

def setModemConfig2():
    global _currentSF
    config = (_currentSF << 4) | (0x4)
    spiX.write(0x1E, config)

def setPout(pout):
    global _currentPower
    if pout >= 2 or pout <= 17:
        outPow = pout - 2
        spiX.write(0x09, 0x80 | outPow)
        _currentPower = pout
    else:
        print("ERROR: Power not changed")
        print("Power must be between +2dBm and +17dBm")

def setBoostPower(bp):
    _currentBP = bp
    if bp == False:
        spiX.write(0x4D, 0x84)
    else:
        spiX.write(0x4D, 0x87)
        print("Warning: only works if Pout = 17dBm")
        print("Warning: ensure 1% Duty Cycle")

def setMode(mode):
    spiX.write(0x01, mode)

def getRSSI():
    rssi = spiX.read(0x1A)
    rssi = -157 + rssi
    return rssi



def readPackets():
    dataLength = spiX.read(0x13)
    bufferStartAddress = spiX.read(0x10)
    
    spiX.write(0x0D, bufferStartAddress)  # sets read addr for SPI
    rxBuf = spiX.burstRead(0x00, dataLength)
    # print(rxBuf)
    rxMode()
    return rxBuf

def rxMode():
    spiX.write(0x40, 0x00)  # G0 interrupt on RX Done
    setMode(M_RX) 
    spiX.write(0x12, 0xFF)  # clear all interrupt flags

def txData(data):
    if type(data) == str:
        data = bytearray(data, 'utf-8')
    elif type(data) == int:
        data = bytes([data])
    else:
        data = bytes(data)
    
    spiX.write(0x0D, 0x00)  # sets SPI buffer address to 0
    spiX.burstWrite(0x00, data)  # write payload to LoRa buffer
    spiX.write(0x22, len(data))  # sets payload length
    spiX.write(0x40, 0x40)  # G0 interrupt on TX Done
    spiX.write(0x12, 0xFF)  # clear all interrupt flags
    setMode(M_TX)
    

def init():
    _rst.low()
    time.sleep(0.1)
    _rst.high()
    time.sleep(0.1)

    if spiX.read(0x42) != 0x12:
        raise Exception("ERROR: RFM not detected")
    else:
        print("RFM95 detected")
    
    setMode(M_LORA)  # LoRa Mode
    time.sleep(0.01)
    if spiX.read(0x01) != 0x80:
        raise Exception("Failed to set RFM to LoRa Mode")
    spiX.write(0x0E, 0x00)  # sets rx and tx buffer pointers to 0
    spiX.write(0x0F, 0x00)
    setModemConfig1()
    spiX.write(0x06, 0xE4)  # sets freq to 915MHz
    spiX.write(0x07, 0xC0)  # I dont understand the math, but this works
    spiX.write(0x08, 0x00)
    setBoostPower(False)
    setPout(17)
    spiX.write(0x39, 0x7A)  # sets the sync word
    setMode(M_STDBY)
    time.sleep(0.1)
    
    rxMode()






# Miscellaneous Functions
def printBW():
    print("Available bandwidths:")
    for key in _bwDict.keys():
        print("  ", key, "kHz")

def printCodingRates():
    print("Available coding rates:")
    for key in _codingRateDict.keys():
        print("  4/",key)

def printSF():
    print("Available spreading factors:")
    for i in range(6,13):
        print("  ", i, ":", 2 ** i, "chips")


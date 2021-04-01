# main.py - sets up LoRa RFM95W and offers functions to run change configuration and run tests

from machine import SPI, Pin
from rfm import printBW, printCodingRates, printSF
import time, rfm, utime, os

g0 = Pin(14, Pin.IN)
g0.irq(lambda pin: rx(), Pin.IRQ_RISING)
logName = "log"
txCount = 0
txStartTime = 0
txEndTime = 0
txLength = 0

def intro():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to LoRa Test. These are the available functions:")
    print("printBW(), printCodingRates(), printSF(), setBW(), setCodingRate(), setSF(), setPout(), setBoostPower(bool)")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

rfm.init()
intro()

def getCurTime():
    curTime = '{:02d}:{:02d}:{:02d}'.format(utime.localtime()[3], utime.localtime()[4], utime.localtime()[5])
    return curTime + " - "

def logEntry(entry):
    with open(logName + ".txt", 'a') as logFile:
        logFile.write("  " + getCurTime() + entry + "\n")

def tx(data):
    global g0, txStartTime, txLength
    txLength = len(data)
    rfm.txData(data)
    txStartTime = utime.ticks_ms()
    g0.irq(lambda pin: txDone(), Pin.IRQ_RISING)

def txDone():
    global g0, txStartTime, txEndTime, txLength

    txEndTime = utime.ticks_ms()
    txDuration = txEndTime - txStartTime
    logEntry("Transmitted "+str(txLength)+" bytes, duration = " + str(txDuration) + "ms")
    print("TX DONE in " + str(txDuration) + "ms")
    rfm.rxMode()
    g0.irq(lambda pin: rx(), Pin.IRQ_RISING)

def rx():
    print("RX DONE")
    
    data = rfm.readPackets()
    print("DATA:", data)
    rssi = rfm.getRSSI()
    print("  RSSI:", rssi)
    logEntry("Received: " + str(data))
    logEntry("  RSSI: " + str(rssi))

def startLog(usrLogName):
    global logName
    logName = usrLogName
    with open(logName + ".txt", 'a') as logFile:
        logFile.write(getCurTime() + "~~New Log Started: " + usrLogName  + "~~\n")
    logConfig()

def sendTest():
    # sends test message of 15-16 bytes
    global txCount
    print("Sending test message")
    tx("test message #" + str(txCount))
    txCount = txCount + 1

def logConfig():
    currentPower = rfm._currentPower
    if currentPower == 17 and rfm._currentBP:
        currentPower = 20
    logEntry("BW: " + str(rfm._currentBW) +
                "kHz, CR: 4/" + str(rfm._currentCodingRate) +
                ", SF: " + str(rfm._currentSF) + 
                ", P: " + str(currentPower) + "dBm")

def setBW(bw):
    rfm.setBW(bw)
    logConfig()

def setCodingRate(cr):
    rfm.setCodingRate(cr)
    logConfig()

def setSF(sf):
    rfm.setSF(sf)
    logConfig()

def setPout(pout):
    rfm.setPout(pout)
    logConfig()

def setBoostPower(bp):
    rfm.setBoostPower(bp)
    logConfig()
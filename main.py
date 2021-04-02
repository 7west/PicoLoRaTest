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
txData = 0

def intro():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to LoRa Test. These are the available functions:")
    print("  printBW(), printCodingRates(), printSF(), setBW(), setCodingRate(),")
    print("  setSF(), setPout(), setBoostPower(bool),")
    print("  defaultConfig(), rangeConfig2(), rangeConfig1(), speedConfig()")
    print("  startLog(), logEntry(), printConfig()")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

if rfm.init():
    print("RFM initialized")
intro()

def getCurTime():
    curTime = '{:02d}:{:02d}:{:02d}'.format(utime.localtime()[3], utime.localtime()[4], utime.localtime()[5])
    return curTime + " - "

def logEntryIndent(entry):
    logEntry("  " + entry)

def logEntry(entry):
    with open(logName + ".txt", 'a') as logFile:
        logFile.write(getCurTime() + entry + "\n")

def tx(data):
    global g0, txStartTime, txData
    txData = data
    rfm.txData(data)
    txStartTime = utime.ticks_ms()
    g0.irq(lambda pin: txDone(), Pin.IRQ_RISING)

def txDone():
    global g0, txStartTime, txEndTime, txData

    txEndTime = utime.ticks_ms()
    txDuration = txEndTime - txStartTime
    logEntryIndent("Transmitted '"+str(txData)+"', duration = " + str(txDuration) + "ms")
    print("TX DONE in " + str(txDuration) + "ms")
    rfm.rxMode()
    g0.irq(lambda pin: rx(), Pin.IRQ_RISING)

def rx():
    print("RX DONE")
    
    data = rfm.readPackets()
    print("DATA:", data)
    rssi = rfm.getRSSI()
    print("  RSSI:", rssi)
    logEntryIndent("Received: " + str(data))
    logEntryIndent("  RSSI: " + str(rssi) + "dBm")

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
    logEntryIndent("BW: " + str(rfm._currentBW) +
                "kHz, CR: 4/" + str(rfm._currentCodingRate) +
                ", SF: " + str(rfm._currentSF) + 
                ", P: " + str(currentPower) + "dBm")

def printConfig():
    currentPower = rfm._currentPower
    if currentPower == 17 and rfm._currentBP:
        currentPower = 20
    print("BW: " + str(rfm._currentBW) +
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

def defaultConfig():
    rfm.setBW(125)
    rfm.setCodingRate(5)
    rfm.setSF(7)
    rfm.setPout(17)
    rfm.setBoostPower(False)
    logConfig()

def rangeConfig1():
    rfm.setBW(125)
    rfm.setCodingRate(7)
    rfm.setSF(10)
    rfm.setPout(17)
    rfm.setBoostPower(False)
    logConfig()

def rangeConfig2():
    rfm.setBW(125)
    rfm.setCodingRate(8)
    rfm.setSF(12)
    rfm.setPout(17)
    rfm.setBoostPower(False)
    logConfig()

def speedConfig():
    rfm.setBW(500)
    rfm.setCodingRate(5)
    rfm.setSF(7)
    rfm.setPout(17)
    rfm.setBoostPower(False)
    logConfig()
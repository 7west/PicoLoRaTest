# main.py - sets up LoRa RFM95W and offers functions to run change configuration and run tests

from machine import SPI, Pin
from rfm import printBW, printCodingRates, printSF
import time, rfm, utime, os

g0 = Pin(14, Pin.IN)
g0.irq(lambda pin: rx(), Pin.IRQ_RISING)
logName = "log"
txCount = 0

rfm.init()

def getCurTime():
    curTime = '{:02d}:{:02d}:{:02d}'.format(utime.localtime()[3], utime.localtime()[4], utime.localtime()[5])
    return curTime + " - "

def logEntry(entry):
    with open(logName + ".txt", 'a') as logFile:
        logFile.write("  " + getCurTime() + entry + "\n")

def tx(data):
    global g0
    rfm.txData(data)
    g0.irq(lambda pin: txDone(), Pin.IRQ_RISING)

def txDone():
    logEntry("Transmitted bytes successfully")
    print("TX DONE")
    rfm.rxMode()
    g0.irq(lambda pin: rx(), Pin.IRQ_RISING)

def rx():
    print("RX DONE")
    
    data = rfm.readPackets()
    print("DATA:", data)
    rssi = rfm.getRSSI()
    print("RSSI:", rssi)
    logEntry("Received: " + str(data))
    logEntry("  RSSI: " + str(rssi))

def startLog(usrLogName):
    global logName
    logName = usrLogName
    with open(logName + ".txt", 'a') as logFile:
        logFile.write(getCurTime() + "~~New Log Started: " + usrLogName  + "~~\n")

def sendTest():
    global txCount
    print("Sending test message")
    tx("test" + str(txCount))
    txCount = txCount + 1


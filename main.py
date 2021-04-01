# main.py - sets up LoRa RFM95W and offers functions to run change configuration and run tests

from machine import SPI, Pin
from rfm import printBW, printCodingRates, printSF
import time, rfm, utime

g0 = Pin(14, Pin.IN)
logName = "log"
txCount = 0

rfm.init()

def getCurTime():
    curTime = str(utime.localtime()[3]) + ":" + str(utime.localtime()[4]) + ":" + str(utime.localtime()[5])
    return curTime + " - "

def logEntry(entry):
    with open(logName + ".txt", 'a') as logFile:
        logFile.write("  " + getCurTime() + entry)

def tx(data):
    global g0
    rfm.txData(data)

    while g0.value() != 1:
        time.sleep(0.001)
    logEntry("Transmitted " + str(len(data)) + " bytes successfully")
    print("TX DONE")

def rx():
    global g0
    rfm.rxMode()
    
    print("Waiting for LoRa message")
    while g0.value() != 1:
        time.sleep(0.001)
    print("RX DONE")
    
    data = rfm.readPackets()
    print("DATA:", data)
    rssi = rfm.getRSSI()
    print("RSSI:", rssi)
    logEntry("Received: " + str(data))

def startLog(usrLogName):
    global logName
    logName = usrLogName
    with open(logName + ".txt", 'a') as logFile:
        logFile.write(getCurTime() + "New Log Started: " + usrLogName)

def sendTest():
    global txCount
    print("Sending test message")
    tx("test" + str(txCount))
    txCount = txCount + 1


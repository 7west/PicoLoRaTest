# rfm.py - 

from machine import Pin
import spiX, time

rst = Pin(15, Pin.OUT)

def init():
    rst.high()
    time.sleep(0.1)

    if spiX.readSpi(0x42) != 0x12:
        raise Exception("ERROR: RFM not detected")
    else:
        print("RFM95 detected")
    
    # other init stuff
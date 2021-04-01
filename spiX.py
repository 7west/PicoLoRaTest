# spiX.py - 

from machine import SPI, Pin
import time

cs = Pin(13, Pin.OUT)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

# cs.low()
# time.sleep(0.01)
# cmd = bytearray([0x42, 0x00])  # should return 0x12
# data = bytearray([0x00,0x00])
# spi.write_readinto(cmd,data)
# print(data)

cs.high()  # running this script multiple times requires cs high
           # cs high ends the transaction and lets you read 
           # any byte after, without it, we read the next address

def read(adr):
    cs.low()
    time.sleep(0.01)
    data = bytearray([0x00,0x00])
    spi.write_readinto(bytearray([adr,0x00]),data)
    cs.high()
    return data[1]

def burstRead(adr, len):
    cs.low()
    time.sleep(0.01)
    spi.write(bytes([adr]))
    dataRead = spi.read(len,0x00)
    cs.high()
    return dataRead

def write(adr, data):
    cs.low()
    time.sleep(0.01)
    adr = adr | 0x80
    msg = bytearray([adr,data])
    spi.write(msg)
    cs.high()

def burstWrite(adr, msg):
    cs.low()
    time.sleep(0.01)
    adr = bytearray([adr | 0x80])
    msg = adr + msg
    spi.write(msg)
    cs.high()
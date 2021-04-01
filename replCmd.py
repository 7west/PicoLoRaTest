# replCmd.py - module to more easily send commands to the Pico via REPL

import serial, time, logging
s = serial.Serial()  # declares the global variable, there might be a better way to do this

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable()

def init(comPort:int):  # PORT8 for tower and PORT12 for laptop
    '''initializes Serial connection with Pico, takes Pico COM#'''
    global s

    s = serial.Serial("COM"+str(comPort), 115200, timeout=1)
    return s.name


def close():  # not recommended, breaks some things with multiple runs
    """closes the Serial connection, do NOT use if you don't plan on restarting the Pico"""
    global s
    s.close()


def _commandHandshake():
    """reads back the command sent and its output, returns all output from Pico"""
    global s

    time.sleep(0.1)  # needs 100 ms to process the longer commands (>4000 bytes)
    logging.debug("in: " + str(s.in_waiting))

    out = bytearray()
    while s.in_waiting > 0:
        out += s.read()
    
    # logging.debug(out.decode())
    return out


def cmd(*cmdInput):
    """sends commands to the Pico, can take command as a string or list of strings
        can also take bytearray for bitstream purposes
        returns: output from command on Pico (not the command echo)"""
    global s
    outLen = 0
    if len(cmdInput) == 1:
        outLen += len(cmdInput[0].encode() + b"\r\n")
        s.write(cmdInput[0].encode() + b"\r\n")
    else:
        for cmdlet in cmdInput:
            if type(cmdlet) is bytearray:
                outLen += len(str(cmdlet).encode())
                s.write(str(cmdlet).encode())
            else:
                outLen += len(cmdlet.encode())
                s.write(cmdlet.encode())
        s.write(b"\r\n")
        outLen += 2

    # return _commandHandshake().decode().split('xZ')[0][outLen:-6]  # this split thing may not work with final configuration
    return _commandHandshake().decode()[outLen:-6]


def cmdBS(cmdInput):
    """Pico REPL command made only for returning bytearray variables from the Pico"""
    global s
    fileLen = int(cmd("len("+cmdInput+")"))
    outLen = len(b"sys.stdout.buffer.write(" + cmdInput.encode() + b")\r\n")
    s.write(b"sys.stdout.buffer.write(" + cmdInput.encode() + b")\r\n")

    return _commandHandshake()[outLen:-(len(str(fileLen)) + 6)]
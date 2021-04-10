#! python3
# recvLog.py - transfers logs from LoRa tests to local computer

import replCmd

replCmd.init(12)
print("Select file (do NOT include 'txt'):")
print("  " + replCmd.cmd("os.listdir()"))
reqFile = input() + ".txt"

replCmd.cmd("reqLog = open('"+reqFile+"','r')")
replCmd.cmd("logStream = reqLog.read()")
replCmd.cmd("reqLog.close()")
replCmd.cmd("import sys")

fileLength = int(replCmd.cmd("print(len(logStream))"))
bitStream = replCmd.cmdBS("logStream")

importedLog = open('logs\\'+reqFile, 'w')
importedLog.write(bitStream.decode())
importedLog.close()
print("Log file: " + reqFile + " saved on computer")
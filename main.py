from pykd import *
import os
import os.path
import sys
from processItem import *

def run():
	if not isKernelDebugging():
		dprintln("this is not kernel debug",True)
		return
		
	if (len(sys.argv) < 2):
		dprintln("please input module name",True)	
		return

	moduleName = sys.argv[1]
	processListString = dbgCommand("!process 0 0",True)
	#skpip first line
	processListString = processListString[processListString.find("\n") + 1:]
	processListString = processListString.strip()
	processList = processListString.split("PROCESS ")

	for processInfoInString in processList:
		if(len(processInfoInString) != 0):
			findModuleInCallStack = False
			tmp = processInfo(processInfoInString)
			for threadDetailInfo in tmp.threadList:
				if("none" == threadDetailInfo.callStack):
					continue

				moduleIndex = threadDetailInfo.callStack.find(moduleName + "!")
				if(moduleIndex != -1):
					if(False == findModuleInCallStack):
						dprintln("********************")
						PrintProcessBaseInfo(tmp)
					findModuleInCallStack = True

					PrintThreadBaseInfo(threadDetailInfo)

			if(True == findModuleInCallStack):
				dprintln("********************")		

#			testPrintProcessInfo(tmp)


def PrintProcessBaseInfo(processInfoStruct):
	dprintln("image name: " + processInfoStruct.imageName + "\n")
	dprintln("process object: " + hex(processInfoStruct.processObjectAddr) + "\n")
	dprintln("cid: " + hex(processInfoStruct.cid) + "\n")
	dprintln("peb: " + hex(processInfoStruct.pebAddr) + "\n")
	dprintln("parentCid: " + hex(processInfoStruct.parentCid) + "\n")
	dprintln("\n\n")

def PrintThreadBaseInfo(tmpThreadInfo):
	dprintln("thread object addr: " + hex(tmpThreadInfo.threadObjectAddr) + "\n")
	dprintln("thread cid: " + tmpThreadInfo.cid + "\n")
	dprintln("thread stack:\n")
	dprintln(tmpThreadInfo.callStack)
	dprintln("\n\n")


def testPrintProcessInfo(processInfoStruct):
		dprintln("********************")
		if(1 == processInfoStruct.error):
			dprintln(processInfoStruct.errorMsg + "\n")
			dprintln(processInfoStruct.processInfoInString + "\n")
			dprintln("********************")
			return

'''
		dprintln("image name: " + processInfoStruct.imageName + "\n")
		dprintln("process object: " + hex(processInfoStruct.processObjectAddr) + "\n")
		if(processInfoStruct.sessionId != "none"):
			dprintln("%s%d%s"%("session id: ",processInfoStruct.sessionId,"\n"))
		else:
			dprintln("%s%s%s"%("session id: ",processInfoStruct.sessionId,"\n"))
		dprintln("cid: " + hex(processInfoStruct.cid) + "\n")
		dprintln("peb: " + hex(processInfoStruct.pebAddr) + "\n")
		dprintln("parentCid: " + hex(processInfoStruct.parentCid) + "\n")
		dprintln("dirBase: " + hex(processInfoStruct.dirBase) + "\n")
		dprintln("objectTable: " + hex(processInfoStruct.objectTableAddr) + "\n")
		dprintln("%s%d%s"%("handleCount: ",processInfoStruct.handleCount,"\n"))
		dprintln("********************")
		for tmpThreadInfo in processInfoStruct.threadList:
			dprintln("thread object addr: " + hex(tmpThreadInfo.threadObjectAddr) + "\n")
			dprintln("thread cid: " + tmpThreadInfo.cid + "\n")
			dprintln("thread stack:\n")
			dprintln(tmpThreadInfo.callStack)
			dprintln("\n")

		dprintln("********************")
'''


if __name__ == "__main__":
	run()	
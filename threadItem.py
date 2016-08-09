from pykd import *
import string

class threadInfo:
	def parserThreadInfoInString(self,threadInfoInString):
		cidStartIndex = threadInfoInString.find("Cid ")
		if(-1 == cidStartIndex):
			self.error = 1
			self.errorMsg = "can not find thread object address"
			self.threadInfoInString = threadInfoInString
			return

		threadObjectAddrInString = threadInfoInString[0:cidStartIndex]
		threadObjectAddrInString = threadObjectAddrInString.strip()
		self.threadObjectAddr = int(threadObjectAddrInString,16)

		threadInfoInString = threadInfoInString[cidStartIndex:]
		tebStartIndex = threadInfoInString.find("Teb: ")
		if(tebStartIndex != -1):
			cidInString = threadInfoInString[len("Cid "):tebStartIndex]
			cidInString = cidInString.strip()
			self.cid = cidInString
		else:
			self.cid = "none"

		if(tebStartIndex != -1):
			threadInfoInString = threadInfoInString[tebStartIndex:]
			win32ThreadStartIndex = threadInfoInString.find("Win32Thread: ")
			if(win32ThreadStartIndex != -1):
				tebInString = threadInfoInString[len("Teb: "):win32ThreadStartIndex]
				tebInString = tebInString.strip()
				self.teb = int(tebInString,16)
			else:
				self.teb = 0
		else:
			self.teb = 0

		#now get call stack
		threadDetailInfoCmd = "!thread %x"%(self.threadObjectAddr)
		threadDetailInfo = dbgCommand(threadDetailInfoCmd)
		CallStackStartIndex = threadDetailInfo.find("Child-SP")
		if(-1 == CallStackStartIndex):
			self.callStack = "none"
		else:
			threadDetailInfo = threadDetailInfo[CallStackStartIndex:].strip()
			self.callStack = threadDetailInfo


	def __init__(self,threadInfoInString):
			self.error = 0
			self.parserThreadInfoInString(threadInfoInString)	
from pykd import *
import string
from threadItem import *

class processInfo:
	def parserInfoInString(self,processInfoInString):
		processObjectAddrEndIndex = processInfoInString.find("\n")

		if(-1 == processObjectAddrEndIndex):
			self.error = 1
			self.errorMsg = "can not find process object address"
			self.processInfoInString = processInfoInString
			return
			
		processObjectAddrInString = processInfoInString[0:processObjectAddrEndIndex]
		processObjectAddrInString = processObjectAddrInString.strip()
		self.processObjectAddr = int(processObjectAddrInString,16)

		processInfoInString = processInfoInString[processObjectAddrEndIndex:]
		sessionIdStartIndex = processInfoInString.find("SessionId: ")
		cidStartIndex = processInfoInString.find("Cid: ")
		if((sessionIdStartIndex != -1) and (cidStartIndex != -1)):
			SessionIdInString = processInfoInString[sessionIdStartIndex + len("SessionId: "):cidStartIndex - 1]
			SessionIdInString = SessionIdInString.strip()
			if(SessionIdInString != "none"):
				self.sessionId = int(SessionIdInString,16)
			else:
				self.sessionId = "none"
		else:
			self.sessionId = "none"

		if(cidStartIndex != -1):	
			processInfoInString = processInfoInString[cidStartIndex:]	
			pebStartIndex = processInfoInString.find("Peb: ")
			if((cidStartIndex != -1) and (pebStartIndex != -1)):
				cidInString = processInfoInString[len("Cid: "):pebStartIndex - 1]
				cidInString = cidInString.strip()
				self.cid = int(cidInString,16)
			else:
				self.cid = 0
		else:
			self.cid = 0
			pebStartIndex = processInfoInString.find("Peb: ")		
		if(pebStartIndex != -1):	
			processInfoInString = processInfoInString[pebStartIndex:]
			parentCidStartIndex = processInfoInString.find("ParentCid: ")
			if((pebStartIndex != -1) and (parentCidStartIndex != -1)):
				pebInString = processInfoInString[len("Peb: "):parentCidStartIndex - 1]
				pebInString = pebInString.strip()
				self.pebAddr = int(pebInString,16)
			else:
				self.pebAddr = 0
		else:
			self.pebAddr = 0
			parentCidStartIndex = processInfoInString.find("ParentCid: ")		

		if(parentCidStartIndex != -1):	
			processInfoInString = processInfoInString[parentCidStartIndex:]
			dirBaseStartIndex = processInfoInString.find("DirBase: ")
			if((parentCidStartIndex != -1) and (dirBaseStartIndex != -1)):
				ParentCidInString = processInfoInString[len("ParentCid: "):dirBaseStartIndex - 1]
				ParentCidInString = ParentCidInString.strip()
				self.parentCid = int(ParentCidInString,16)
			else:
				self.parentCid = 0
		else:
			self.parentCid = 0
			dirBaseStartIndex = processInfoInString.find("DirBase: ")

		if(dirBaseStartIndex != -1):	
			processInfoInString = processInfoInString[dirBaseStartIndex:]
			objectTableStartIndex = processInfoInString.find("ObjectTable: ")
			if((dirBaseStartIndex != -1) and (objectTableStartIndex != -1)):
				dirBaseInString = processInfoInString[len("DirBase: "):objectTableStartIndex - 1]
				dirBaseInString = dirBaseInString.strip()
				self.dirBase = int(dirBaseInString,16)
			else:
				self.dirBase = 0
		else:
			self.dirBase = 0
			objectTableStartIndex = processInfoInString.find("ObjectTable: ")		
				
		if(objectTableStartIndex != -1):		
			processInfoInString = processInfoInString[objectTableStartIndex:]
			handleCountStartIndex = processInfoInString.find("HandleCount: ")
			if((objectTableStartIndex != -1) and (handleCountStartIndex != -1)):
				objectTableInString = processInfoInString[len("ObjectTable: "):handleCountStartIndex - 1]
				objectTableInString = objectTableInString.strip()
				self.objectTableAddr = int(objectTableInString,16)
			else:
				self.objectTableAddr = 0
		else:
			self.objectTableAddr = 0
			handleCountStartIndex = processInfoInString.find("HandleCount: ")	

		if(handleCountStartIndex != -1):
			processInfoInString = processInfoInString[handleCountStartIndex:]
			imageStartIndex = processInfoInString.find("Image: ")
			if((handleCountStartIndex != -1) and (imageStartIndex != -1)):
				handleCountInString = processInfoInString[len("HandleCount: "):imageStartIndex - 1]
				handleCountInString = handleCountInString.strip()
				if('.' == handleCountInString[-1]):
					handleCountInString = handleCountInString[0:-1]
				self.handleCount = int(handleCountInString,10)
			else:
				self.handleCount = 0
		else:
			self.handleCount = 0
			imageStartIndex = processInfoInString.find("Image: ")
				
		if(imageStartIndex != -1):		
			processInfoInString = processInfoInString[imageStartIndex:]
			imageInString = processInfoInString[len("Image: "):]
			imageInString = imageInString.strip()
			self.imageName = imageInString		
		else:
			self.imageName = ""	


	def __init__(self,processInfoInString):
		self.error = 0
		self.threadList = []
		self.parserInfoInString(processInfoInString)
		if(self.error != 1):
			#now parser thread info
			processDetailInfoCmd = "%s %x 4"%("!process",self.processObjectAddr)
			if(False == str.isdigit(processDetailInfoCmd[-1])):
				processDetailInfoCmd = processDetailInfoCmd[0:-1]

			processDetailInString = dbgCommand(processDetailInfoCmd,True)	
			threadInfoStartIndex = processDetailInString.find("THREAD ")

			if(-1 == threadInfoStartIndex):
				self.error = 1
				self.errorMsg = "can not get thread info"
				return
			else:
				threadInfoInString = processDetailInString[threadInfoStartIndex:]
				threadInfoInString.strip()
				threadInfoList = threadInfoInString.split("THREAD ")
				for threadInfoInString in threadInfoList:
					if(0 == len(threadInfoInString)):
						continue
					tmpThreadInfo = threadInfo(threadInfoInString)	
					if(0 == tmpThreadInfo.error):
						self.threadList.append(tmpThreadInfo)


		


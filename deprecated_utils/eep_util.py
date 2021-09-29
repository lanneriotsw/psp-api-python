                                                                                                                   

from __future__ import print_function
import time
from ctypes import *
import sys,os,string

#import library
#--------------------------------------------------------------------#

cdll.LoadLibrary("/usr/local/lib/liblmbio.so")  
lib=cdll.LoadLibrary("/usr/local/lib/liblmbapi.so")


#--------------------------------------------------------------------#
def _err_print(pbString):

	print("\033[1;31m {:s} \033[0m".format(pbString)) 
#--------------------------------------------------------------------#

def __print_usage(argv0):

	print("Usage: {:s} -s0/../-s8 -byte/-word/-dword -addr #hex -read".format(argv0))
	print("       {:s} -s0/../-s8 -byte/-word/-dword -addr #hex -write #hex".format(argv0))
	print("       {:s} -s0/../-s8 -wrblock  \"wrtie_string\" -addr #hex ".format(argv0))
	print("       {:s} -s0/../-s8 -rdblock  -addr #hex -length #dec".format(argv0))
	print("       {:s} -s0/../-s8 -erase".format(argv0))
	print("       {:s} -s0/../-s8 -test [-c textfile]  --> for testing".format(argv0))
	print("       {:s} -query			   --> report all eeprom slot".format(argv0))
	print("	paramerer:")
	print("	-s0/../-s8 	: assign slot device number, -s0 is onboard device")
	print("	-erase		: erase EEPROM all content to value 0")
	print("	-read/-write	: read or write access")
	print("	-addr #hex	: assign data address of EEPROM device")

#--------------------------------------------------------------------#


def _print_error_message( pstrFunc, errcode):

	print("\033[1;31m{:s} return error code = 0x{:08X}, ".format(pstrFunc, errcode&0xFFFFFFFF),end="")

	if errcode == -1:
		_err_print("Function Failure")
		
	elif errcode == -2:
		_err_print("Library file not found or not exist")
		
	elif errcode == -3:
		_err_print("Library not opened yet")
		
	elif errcode == -4:
		_err_print("Parameter invalid or out of range")
		
	elif errcode == -5:
		_err_print("This functions is not support of this platform")
		
	elif errcode == -6:
		_err_print("busy")
		
	elif errcode == -7:
		_err_print("the API library is not matched this platform")
		
	elif errcode == -8:
		_err_print("the lmbiodrv driver or i2c-dev drvive no loading")
		
	else :
		print(""),
	
	print("\033[m")

#--------------------------------------------------------------------#


TYPE_BYTE	=1
TYPE_WORD	=2
TYPE_DWORD	=3
TYPE_TEST	=4
TYPE_QUERY	=5
TYPE_ERASE	=6
TYPE_WRBLOCK	=7
TYPE_RDBLOCK	=8

CMD_READ	=0
CMD_WRITE	=1

ERR_Success	=0

MAX_FILE_SIZE	=1024*2
MAX_EEP_SIZE	=256

CONFIG_NAME= "testeep.txt"

def eep_util():


	iRet,index,xi= 0,0,1
	argc=len(sys.argv)
	ubBlock=create_string_buffer(256)
	dwAddr,iBlockLen=0,-1
	bData ,wData ,dwData= c_uint8(),c_uint16(),c_uint32()
	bSlot=0xFF
	bType = 0
	bSubType = CMD_READ
	global CONFIG_NAME
	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 

	if  argc < 2  :
		__print_usage(sys.argv[0])
		return -1
	
	while  xi < argc :

		if 	"-s0" == sys.argv[xi] :
			bSlot = 0
			xi += 1
		elif 	"-s1" == sys.argv[xi] :
			bSlot = 1
			xi += 1
		elif 	"-s2" == sys.argv[xi] :
			bSlot = 2
			xi += 1
		elif 	"-s3" == sys.argv[xi] :
			bSlot = 3
			xi += 1
		elif 	"-s4" == sys.argv[xi] :
			bSlot = 4
			xi += 1
		elif 	"-s5" == sys.argv[xi] :
			bSlot = 5
			xi += 1
		elif 	"-s6" == sys.argv[xi] :
			bSlot = 6
			xi += 1
		elif 	"-s7" == sys.argv[xi] :
			bSlot = 7
			xi += 1
		elif 	"-s8" == sys.argv[xi] :
			bSlot = 8
			xi += 1
		elif 	"-byte" == sys.argv[xi] :
			bType = TYPE_BYTE
			xi += 1
		elif 	"-word" == sys.argv[xi] :
			bType = TYPE_WORD
			xi += 1
		elif 	"-dword" == sys.argv[xi] :
			bType = TYPE_DWORD
			xi += 1
		elif 	"-read" == sys.argv[xi] :
			bSubType = CMD_READ
			xi += 1
		elif 	"-erase" == sys.argv[xi] :
			bType = TYPE_ERASE
			xi += 1
		elif 	"-test" == sys.argv[xi] :
			bType = TYPE_TEST
			xi += 1
		elif    "-wrblock" == sys.argv[xi] :
			if xi == (argc-1)	:
				print("<Warning> not input string data")
				return -1
			bType = TYPE_WRBLOCK
			ubBlock = sys.argv[xi+1]
			xi += 2
		elif	"-rdblock" == sys.argv[xi] :
			bType = TYPE_RDBLOCK
			xi += 1
		elif	"-length" == sys.argv[xi] :
			if xi == argc-1 :
				print("<Warning> not input length")
				return -1
			iBlockLen = int(sys.argv[xi+1])
			xi += 2
		elif	"-query" == sys.argv[xi] :
			bType = TYPE_QUERY
			bSlot = 0
			xi += 1
		elif	"-c" == sys.argv[xi] :
			if xi == argc-1 :
				print("<Warning> not input length")
				return -1
			CONFIG_NAME = sys.argv[xi+1]
			xi += 2
		elif	"-write" == sys.argv[xi] :
			if xi == argc-1 :
				print("<Warning> not input length")
				return -1
			bSubType = CMD_WRITE
			dwData = sys.argv[xi+1]
			dwData = int(dwData,base=16)
			print("Write Data is 0x{:02X}".format(dwData))
			xi += 2
		elif	"-addr" == sys.argv[xi] :
			if xi == argc-1 :
				print("<Warning> not input length")
				return -1
			dwAddr = sys.argv[xi+1]
			dwAddr = int(dwAddr,base=16)
			print("EEPROM address is 0x{:02X}".format(dwAddr))
			xi += 2
		else :
			__print_usage(sys.argv[0])
			return -1
	if ( bSlot == 0xFF) :
		__print_usage(sys.argv[0])
		return -1
	
	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 
	if	bType == TYPE_BYTE :
		if bSubType == CMD_WRITE :
			if dwData > 0xFF :
				print("<warning> write data out of range")
				return -1
			bData = dwData & 0xff
			print(type(bData))
			iRet = lib.LMB_EEP_WriteByte(bSlot, dwAddr, bData)
			if  iRet == ERR_Success  :
				print("Write byte Addr=0x{:0X}({:d}), Data=0x{:02X}({:d})".format(dwAddr, dwAddr, bData, bData))
			else :
				_print_error_message("LMB_EEP_WriteByte", iRet)
		else:

			iRet = lib.LMB_EEP_ReadByte(bSlot, dwAddr, byref(bData))
			if ( iRet == ERR_Success ) :
				print("Read byte Addr=0x{:0X}({:d}), Data=0x{:02X}({:d})".format(dwAddr, dwAddr, bData.value, bData.value))
			else	:
				 _print_error_message("LMB_EEP_ReadByte", iRet)
	elif	bType == TYPE_WORD:
		if bSubType == CMD_WRITE :
			if dwData > 0xFFFF :
				print("<warning> write data out of range")
				return -1
			wData = dwData & 0xffff
			iRet = lib.LMB_EEP_WriteWord(bSlot, dwAddr, wData)
			if  iRet == ERR_Success  :
				print("Write byte Addr=0x{:0X}({:d}), Data=0x{:04X}({:d})".format(dwAddr, dwAddr, wData, wData))
			else :
				_print_error_message("LMB_EEP_WriteByte", iRet)
		else:
			iRet = lib.LMB_EEP_ReadWord(bSlot, dwAddr, byref(wData))
			if ( iRet == ERR_Success ) :
				print("Read byte Addr=0x{:0X}({:d}), Data=0x{:04X}({:d})".format(dwAddr, dwAddr, wData.value, wData.value))
			else	:	  
				 _print_error_message("LMB_EEP_ReadByte", iRet)
	elif	bType == TYPE_DWORD:
		if bSubType == CMD_WRITE :
			iRet = lib.LMB_EEP_WriteDWord(bSlot, dwAddr, dwData)
			if  iRet == ERR_Success  :
				print("Write byte Addr=0x{:0X}({:d}), Data=0x{:08X}({:d})".format(dwAddr, dwAddr, dwData, dwData))
			else :
				_print_error_message("LMB_EEP_WriteByte", iRet)
		else:
			iRet = lib.LMB_EEP_ReadDWord(bSlot, dwAddr, byref(dwData))
			if ( iRet == ERR_Success ) :
				print("Read byte Addr=0x{:0X}({:d}), Data=0x{:08X}({:d})".format(dwAddr, dwAddr, dwData.value, dwData.value))
			else	:	  
				 _print_error_message("LMB_EEP_ReadByte", iRet)

	elif	bType ==TYPE_TEST :
		_eep_tst(bSlot)
	elif	bType ==TYPE_QUERY :
		_eep_query()
	elif	bType ==TYPE_ERASE :
		iRet=lib.LMB_EEP_Erase(bSlot)
		if iRet == ERR_Success :
			print("Slot-{:d} EEPROM erase ok".format(bSlot))
		else	:	  
			_print_error_message("LMB_EEP_Erase", iRet)
	elif	bType ==TYPE_WRBLOCK :
		iBlockLen = len(ubBlock)
		iRet = lib.LMB_EEP_WriteBlock(bSlot , dwAddr, iBlockLen, ubBlock)
		if ( iRet == ERR_Success ) :
			print("Write block Addr=0x{:0X}({:d}), Length={:d}, Data={:s}".format(dwAddr, dwAddr,iBlockLen,ubBlock))
		else	:	  
			_print_error_message("LMB_EEP_WriteBlock", iRet)
	elif	bType ==TYPE_RDBLOCK :
		if ( iBlockLen == -1 ) :
			print("<Error> no input block read length !!!")
		else:	
			memset(ubBlock,0,256)
			iRet = lib.LMB_EEP_ReadBlock(bSlot , dwAddr, iBlockLen, ubBlock)
			if ( iRet == ERR_Success ) :
				print("Write block Addr=0x{:0X}({:d}), Length={:d}, Data={:s}".format(dwAddr, dwAddr,iBlockLen,ubBlock.value))
			else	:	  
				_print_error_message("LMB_EEP_ReadBlock", iRet)
	else:
		__print_usage(sys.argv[0])
		return -1



	lib.LMB_DLL_DeInit()
	return iRet
#--------------------------------------------------------------------#

def _eep_tst(bSlot):

	ubWrData,ubRdData=create_string_buffer(256),create_string_buffer(256)
	ubBlock,ubBackup=create_string_buffer(256),[0]*256
	dwAddr=c_uint32()
	bData ,wData ,dwData= c_uint8(),c_uint16(),c_uint32()
	errCnt,i,bResult=0,0,1
	global CONFIG_NAME

	if os.path.isfile(CONFIG_NAME) != 1  :
		print("\033[1;34m<Note> Not found {:s} file, uses default /etc/lanner/testeep.txt !!!\033[m".format(CONFIG_NAME))
		CONFIG_NAME="/etc/lanner/testeep.txt"
		if( os.path.isfile(CONFIG_NAME) != 1 ) :
			print("\033[1;31m<Warning> Not found boundary vaule file !!!\033[m")

	

	iRet = lib.LMB_DLL_Init()
	if ( iRet != ERR_Success ) :
		_print_error_message("LMB_DLL_Init", iRet)
		print("please confirm the API librraies is matched this platform")
		return -1
	
#	//add backup EEPROM content
	print("====> backup EEPROM content ...... ",end='')
	sys.stdout.flush()
	for xi in range(256) :
		iRet = lib.LMB_EEP_ReadByte(bSlot, xi, byref(bData))
		ubBackup[xi]=chr(bData.value)
		if ( iRet != ERR_Success ) :
			_print_error_message("LMB_EEP_ReadByte", iRet)
			errCnt+=1
		if ( errCnt >= 3 ):
			print("\033[1;31m<Error> maybe slot not exist !!!\033[m")
			return -1
	
	print("OK")
#	//*********  write data from file *******/
#		//buf=(char*)malloc(sizeof(char))
	buf=create_string_buffer(MAX_FILE_SIZE)
	inf = open(CONFIG_NAME,"r")

	#//in = fopen("test.txt","r")
	if( None == inf) :
		print("\033[1;31m<Error> not found file %s\033[m", CONFIG_NAME)
		return 0
	
	read_buf=inf.read(1)
#	print(read_buf)
	buf.value=read_buf
#		//load initialization file
	while read_buf != '' : 
		i+=1
		assert( i < MAX_EEP_SIZE ) #//file too big, you can redefine MAX_FILE_SIZE to fit the big file 
		read_buf=inf.read(1)
		#print(read_buf)
		buf.value+=read_buf

#	print(buf.value)		
	inf.close()
	wrLeng=i
#	//iRet = iRet = LMB_EEP_Erase(bSlot)
#	//if ( iRet != ERR_Success ) _print_error_message("LMB_EEP_Erase", iRet)
	memset(ubWrData, 0, 256)
	index=0
	print("write data: ")
	for wAddr in range(i):
#		print(buf[wAddr])
		bData = (buf[wAddr])
		ubWrData[index] = bData
		index += 1
		iRet = lib.LMB_EEP_WriteByte(bSlot, wAddr,ord(bData))
		if ( iRet == ERR_Success ) :
			print("{:s}".format(bData),end='')
		else			   :
 			_print_error_message("LMB_EEP_WriteByte", iRet)
			errCnt+=1
		if ( errCnt >= 3 ) :
			print("\033[1;31m<Error> maybe slot not exist !!!\033[m")
			return -1
#	/*******  read data **********/
	memset(ubRdData, 0, 256)
	index=0
	bData=c_uint8()
	print("read data : ")
	for wAddr in range(i):
	
		iRet = lib.LMB_EEP_ReadByte(bSlot, wAddr,byref(bData))	
		ubRdData[index]=chr(bData.value)
#		print(ubRdData[index])
		index += 1
		if ( iRet == ERR_Success ) :
			print("{:c}".format(bData.value),end='')
		else			   :
			_print_error_message("LMB_EEP_ReadByte", iRet)
	
	for xxi in range(wrLeng) :
		if ( ubRdData[xxi] != ubWrData[xxi] ) :
			bResult=0
	
	if ( bResult )  :
		print("EEPROM Write/Read compared ==> OK")
	else 		:
		print("EERPOM Write/Read compared ==> ALARM")
	
#	//add restore EEPROM content
	print("====> restore EEPROM content ...... ",end='')
	sys.stdout.flush()
	for xi in range(256):
		bData = ubBackup[xi]
#		print(bData)
		iRet = lib.LMB_EEP_WriteByte(bSlot, xi, ord(bData))
		if ( iRet != ERR_Success ) :
			_print_error_message("LMB_EEP_WriteByte", iRet)
			errCnt+=1
		if ( errCnt >= 3 ) :
			print("\033[1;31m<Error> maybe slot not exist !!!\033[m")
			return -1
	
	print("OK")
#	//add check restore EEPROM content
	bData=c_uint8()
	for xi in range(256) :
		iRet = lib.LMB_EEP_ReadByte(bSlot, xi, byref(bData))
		ubRdData[xi]=chr(bData.value)
#		print(ubRdData[xi])
		if ( iRet != ERR_Success ) :
			_print_error_message("LMB_EEP_ReadByte", iRet)
			errCnt+=1
		if ( errCnt >= 3 ) :
			print("\033[1;31m<Error> maybe slot not exist !!!\033[m")
			return -1
	for xxi in range(wrLeng) :
#		print(ubRdData[xxi])
		if ( ubRdData[xxi] != ubBackup[xxi] ) :
			bResult=0
		
	if ( bResult )  :
		print("EEPROM Write/Read compared ==> OK")
	else 		:
		print("EERPOM Write/Read compared ==> ALARM")

	lib.LMB_DLL_DeInit()

	
	return 0



#--------------------------------------------------------------------#

def _eep_query():
	iRet=0
	uwSlotsDev=c_uint16(0)
	iRet = lib.LMB_EEP_QueryDevices(byref(uwSlotsDev))
	if ( iRet == ERR_Success ) :
		print("EEPROM devises exist 0x{:04X}".format(uwSlotsDev.value))
	else			   :
		_print_error_message("LMB_EEP_QueryDevices", iRet)



if __name__ == '__main__':
	eep_util()

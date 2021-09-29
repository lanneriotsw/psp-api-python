                                                                                                                

from __future__ import print_function
import time
from ctypes import *
import sys,os,string
import random
#import library
#--------------------------------------------------------------------#

cdll.LoadLibrary("/usr/local/lib/liblmbio.so")  
lib=cdll.LoadLibrary("/usr/local/lib/liblmbapi.so")

#--------------------------------------------------------------------#
def _err_print(pbString):

	print("\033[1;31m {:s} \033[0m".format(pbString)) 
#--------------------------------------------------------------------#

def __print_usage(argv0):

	print("Usage: {:s} -gpo -w -data hex 		 --> write GPO data".format(argv0))
	print("       {:s} -gpo -wpin 1/../4 -set/-reset --> write GPO pin data".format(argv0))
	print("       {:s} -gpo/-gpi -r 		 --> read GPO/GPI data".format(argv0))
	print("       {:s} -gpi -rpin 1/../4 		 --> read GPI pin data".format(argv0))
	print("       {:s} -callback".format(argv0))

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

class INTRUSION_TIME(Structure):
	_fields_=[("uwYear",c_uint16),("ubMonth",c_uint8),("ubDay",c_uint8),("ubHour",c_uint8),("ubMinute",c_uint8),("ubSecond",c_uint8)]
class GPI_MSG(Structure):
	_fields_=[("ubGroup",c_uint8),("udwGpis",c_uint32),("udwStatus",c_uint32),("stuTime",INTRUSION_TIME)]

c_callback=CFUNCTYPE(None,GPI_MSG)
def GpiCallback(stuGpiMsg) :
	count = 1
	print("GPI Item = {:02X}, Status = {:02X}, time is {:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(stuGpiMsg.udwGpis, stuGpiMsg.udwStatus, stuGpiMsg.stuTime.uwYear, stuGpiMsg.stuTime.ubMonth, stuGpiMsg.stuTime.ubDay,stuGpiMsg.stuTime.ubHour, stuGpiMsg.stuTime.ubMinute, stuGpiMsg.stuTime.ubSecond))

p_callback=c_callback(GpiCallback)
#--------------------------------------------------------------------#

def _exec_callback():

	iRet = 0
	xloop = 100
	stuGpiMsg=GPI_MSG()
	lib.LMB_GPIO_GpoWrite(0, 0)
	iRet=lib.LMB_GPIO_GpiCallback(p_callback, 150)
	if iRet == ERR_Success :
		print("----> hook GPI Callback OK <----")
	else:
		print("-----> hook GPI callback failure <-------")
		return
 	print("===> wait about 10 second time <===")

	while xloop >0 :
		if xloop == 80:
			random.seed(time.time())
			ubtemp=(random.randint(0,10000) %4 )+1
			print("GPO-{:d} set to 1".format(ubtemp))
			lib.LMB_GPIO_GpoPinWrite(0, ubtemp, 1)
		if xloop == 60:
			random.seed(time.time())
			print("GPO-{:d} set to 0".format(ubtemp))
			lib.LMB_GPIO_GpoPinWrite(0, ubtemp, 0)
		if xloop == 40:
			random.seed(time.time())
			ubtemp=(random.randint(0,10000) %4 )+1
			print("GPO-{:d} set to 1".format(ubtemp))
			lib.LMB_GPIO_GpoPinWrite(0, ubtemp, 1)
		if xloop == 20:
			random.seed(time.time())
			print("GPO-{:d} set to 0".format(ubtemp))
			lib.LMB_GPIO_GpoPinWrite(0, ubtemp, 0)
		time.sleep(0.1)
		xloop -= 1
	iRet = lib.LMB_GPIO_GpiCallback(None, 50)
	if  iRet == ERR_Success  :
		print("----> hook GPI Callback Disable OK <----")

#--------------------------------------------------------------------#

SEL_READ	=1
SEL_WRITE	=2
SEL_READ_PIN	=3
SEL_WRITE_PIN	=4
SEL_GPO		=1
SEL_GPI		=2
SEL_DATA	=1

ERR_Success	=0
#--------------------------------------------------------------------#

def gpio_util():

	iRet,index,xi= 0,0,1
	xloop= 0 ,0 
	argc=len(sys.argv)
	fEnableCB=0
	selIO,selRW,selData=0,0,0
	udwRead,ubData=c_uint32(0),c_uint8(0)

	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 

	if  argc < 2  :
		__print_usage(sys.argv[0])
		return -1

	while  xi < argc :

		if "-gpo" == sys.argv[xi] : 
			selIO = SEL_GPO
			xi += 1
		elif "-gpi" == sys.argv[xi] : 
			selIO = SEL_GPI
			xi += 1
		elif "-r" == sys.argv[xi] : 
			selRW = SEL_READ
			xi += 1
		elif "-w" == sys.argv[xi] : 
			selRW = SEL_WRITE
			xi += 1
		elif "-set" == sys.argv[xi] : 
			ubWrPinData = 1
			xi += 1
		elif "-reset" == sys.argv[xi] : 
			ubWrPinData = 0
			xi += 1
		elif "-callback" == sys.argv[xi] : 
			fEnableCB = 1
			xi += 1
		elif "-rpin" == sys.argv[xi] : 
			selRW = SEL_READ_PIN
			dwPin =	int(sys.argv[xi+1],base=16)	
			print("Read GPI/GPO Pin is {:d}".format(dwPin))	
			xi += 2
		elif "-wpin" == sys.argv[xi] : 
			selRW = SEL_WRITE_PIN
			dwPin =	int(sys.argv[xi+1],base=16)	
			print("Write GPI/GPO Pin is {:d}".format(dwPin))	
			xi += 2
		elif "-data" == sys.argv[xi] : 
			selData = SEL_DATA
			dwData = int(sys.argv[xi+1],base=16)	
			print("Write Data={:d}, 0x{:02X}".format(dwData,dwData))	
			xi += 2
		else :
			__print_usage(sys.argv[0])
			return -1
	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 
	if fEnableCB :
		_exec_callback()	
	else:
		if selIO == 0:
			print("\033[1;31m<Warning> !!! please uses -gpo or -gpi \033[m")
			__print_usage(sys.argv[0])
			return -1
		elif selRW == 0:
			print("\033[1;31m<Warning> !!! please uses -r or -w \033[m")
			__print_usage(sys.argv[0])
			return -1
		elif selRW == SEL_WRITE and selData==0:
			print("\033[1;31m<Warning> !!! please uses -data hex \033[m")
			__print_usage(sys.argv[0])
			return -1

		else:
			if selRW == SEL_READ:
				if selIO == SEL_GPI :
					iRet = lib.LMB_GPIO_GpiRead(0, byref(udwRead))
				else :
					iRet = lib.LMB_GPIO_GpoRead(0, byref(udwRead))
				
				if iRet != 0:
					if selIO == SEL_GPI :
						 _print_error_message("LMB_GPIO_GpiRead", iRet)
					else:
						_print_error_message("LMB_GPIO_GpiRead", iRet)
				else:
					print("==> GPI/O read = 0x{:02X}".format(udwRead.value))
			elif selRW == SEL_READ_PIN:
				if selIO == SEL_GPI :
					iRet = lib.LMB_GPIO_GpiPinRead(0,dwPin, byref(ubData))
				else :
					iRet = lib.LMB_GPIO_GpoPinRead(0,dwPin, byref(ubData))
				if iRet != 0:
					if selIO == SEL_GPI :
						 _print_error_message("LMB_GPIO_GpiPinRead", iRet)
					else:
						_print_error_message("LMB_GPIO_GpoPinRead", iRet)
				else:
					print("==> GPI/O read pin{:d} = {:d}".format(dwPin, ubData.value))
			elif selRW == SEL_WRITE:
				if selIO == SEL_GPI:
					print("\033[1;31m<Warning> !!!  GPI not support write function \033[m")
					return -1
				iRet=lib.LMB_GPIO_GpoWrite(0, dwData)
				if iRet == 0 :
					print("===> GPO write OK")
				else :
					_print_error_message("LMB_GPIO_GpoWrite", iRet)
			elif selRW == SEL_WRITE_PIN:
				if selIO == SEL_GPI:
					print("\033[1;31m<Warning> !!!  GPI not support write function \033[m")
					return -1
				if ubWrPinData == 0xff :
					print("\033[1;31m<Warning> !!!  GPO pin write date not setting\033[m")
					return -1
				iRet=lib.LMB_GPIO_GpoPinWrite(0, dwPin, ubWrPinData)
				if iRet == 0 :
					print("==> GPI/O Write pin{:d} = {:d} OK".format(dwPin, ubWrPinData))
				else :
					_print_error_message("LMB_GPIO_GpoWrite", iRet)
			else:
				return -1


	lib.LMB_DLL_DeInit()
	return iRet
if __name__ == '__main__':
	gpio_util()


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

	print("Usage: {:s} -status		--> read status".format(argv0))
	print("       {:s} -callback		--> uses callback detect".format(argv0))
	print("       {:s} -test [seconds]	--> for testing (default: 5 seconds)".format(argv0))

#--------------------------------------------------------------------#
def _show_delay(sec):

	index=sec
	while ( index>0) :
		print("{:d}. ".format(index),end="")
		sys.stdout.flush()
		index -= 1
		time.sleep(1)
	
	print("{:d}.".format(index))


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

class INTRUSION_MSG(Structure):
	_fields_=[("udwOccurItem",c_uint32),("udwStatus",c_uint32),("stuTime",INTRUSION_TIME)]

c_callback=CFUNCTYPE(None,INTRUSION_MSG)

def swrCallback(stuGpiMsg) :
	count = 1
	print("SWR Item  = {:04X}, Status = {:04X}, time is {:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(stuGpiMsg.udwOccurItem, stuGpiMsg.udwStatus, stuGpiMsg.stuTime.uwYear, stuGpiMsg.stuTime.ubMonth, stuGpiMsg.stuTime.ubDay,stuGpiMsg.stuTime.ubHour, stuGpiMsg.stuTime.ubMinute, stuGpiMsg.stuTime.ubSecond))

p_callback=c_callback(swrCallback)
#--------------------------------------------------------------------#
def _exec_callback() :

	iRet=0
	xloop = 100;
	
	#//SWR callback test
	iRet = lib.LMB_SWR_IntrCallback(p_callback, 150)
	if   iRet == ERR_Success  :
		print("----> hook Software-Reset button Callback OK <----");
	else 	:
		print("-----> hook Software-Reset button callback failure <-------");
		return ; 
	
	print("===> wait about 10 second time <===");
	
	while(xloop>0) :
		time.sleep(0.1)
		xloop-=1
	
	iRet = lib.LMB_SWR_IntrCallback(None, 150);
	if   iRet == ERR_Success  :
		print("----> disabled Software-Reset button Callback hook <----");


#--------------------------------------------------------------------#
ERR_Success	=0

PSU_WATTS_INPUT	=0
PSU_WATTS_OUTPUT=1

wtime=5
#--------------------------------------------------------------------#

def swr_util():

	iRet,index,xi= 0,0,1
	argc=len(sys.argv)
	ubRead=c_uint8()
	global wtime



	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 
	if  argc < 2  :
		__print_usage(sys.argv[0])
		return -1

	while  xi < argc :

		if "-status" == sys.argv[xi] : 
			bsel = 1
			xi += 1
		elif "-callback" == sys.argv[xi] : 
			bsel = 2
			xi += 1
		elif "-test" == sys.argv[xi] : 
			bsel = 3
			if argc > 2 :
				wtime=int(sys.argv[2])
				xi+=1
			xi += 1
		else :
			print("\033[1;31m<Error> Input parameter invaild \033[m")
			__print_usage(sys.argv[0])
			return -1

	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 
	if bsel == 1 :
		iRet = lib.LMB_SWR_GetStatus(byref(ubRead))
		if  iRet == ERR_Success :
			print("SWReset button Status is {:d}".format(ubRead.value))
		else 	:
			_print_error_message("LMB_SWR_GetStatus".format(iRet))
	elif bsel == 2 :
		_exec_callback()
	elif bsel == 3 :
		_swr_tst()

	return iRet

def _swr_tst():
	global wtime
	ubRead=c_uint8()
	dwCnt=0
	index=wtime
	itime=wtime

	print("===> wait {:d} seconds for Software Reset Button trigger .......".format(itime)) 
	while (1) :
		if ( (dwCnt % 10) == 0) :
			print("{:d}. ".format(index),end='')
			sys.stdout.flush()
			index -= 1
		

		lib.LMB_SWR_GetStatus(byref(ubRead))
		if ( ubRead.value ) :
			break
		
		dwCnt += 1
		if ( dwCnt > (itime*10) ) :
			break
		time.sleep(0.1)
	
	print("");
	if ( ubRead.value==1  ) :
		print("Software/Reset button pressed ! --> OK")
	else :
		print("\033[1;31mSoftware/Reset button not deteced ! --> ALARM\033[0m")


if __name__ == '__main__':
	swr_util()


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

	print("Usage: {:s} -config seconds".format(argv0))
	print("       {:s} -start [seconds]".format(argv0))
	print("       {:s} -reload".format(argv0))
	print("       {:s} -stop".format(argv0)) 

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
ERR_Success	=0

WDT_START	=1
WDT_STOP	=2
WDT_RELOAD	=3
WDT_CONFIG	=4

BASE_SECOND	=1
#--------------------------------------------------------------------#

def wdt_util():

	iRet,index,xi= 0,0,1
	argc=len(sys.argv)
	wtime = 0

	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 
	if  argc < 2  :
		__print_usage(sys.argv[0])
		return -1

	while  xi < argc :

		if "-start" == sys.argv[xi] : 
			selMode = WDT_START
			xi += 1
		elif "-stop" == sys.argv[xi] : 
			selMode = WDT_STOP
			xi += 1
		elif "-reload" == sys.argv[xi] : 
			selMode = WDT_RELOAD
			xi += 1
		elif "-config" == sys.argv[xi] : 
			selMode = WDT_CONFIG
			selData = WDT_CONFIG
			if xi == argc-1 :
				print("<Warning> not input timer count")
				return -1
			wCount = int(sys.argv[xi+1])
			print("===> WDT sets {:d} seconds ".format(wCount))
			xi += 2
		else :
			wtime = int(sys.argv[xi])


	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 

	if selMode == WDT_CONFIG:
		if selData == 0 :
			print("<Warning> no input tine count value")
			__print_usage(sys.argv[0])
			return -1
		iRet = lib.LMB_WDT_Config(wCount, BASE_SECOND)
		if iRet == 0:
			print("==> WDT set {:d} seconds OK".format(wCount))
		else :
			_print_error_message("LMB_WDT_Config", iRet)

	elif selMode == WDT_START:
		if wtime != 0 :
			iRet = lib.LMB_WDT_Config(wtime, BASE_SECOND)
			if iRet == 0:
				print("==> WDT set {:d} seconds OK".format(wtime))
			else :
				_print_error_message("LMB_WDT_Config", iRet)
		iRet = lib.LMB_WDT_Start()
		if iRet == 0:
			print("==> WDT starting OK")
		else :
			_print_error_message("LMB_WDT_Start", iRet)

	elif selMode == WDT_STOP:
		iRet = lib.LMB_WDT_Stop()
		if iRet == 0:
			print("==> WDT stop OK")
		else :
			_print_error_message("LMB_WDT_Stop", iRet)

	elif selMode == WDT_RELOAD:
		iRet = lib.LMB_WDT_Tick()
		if iRet == 0:
			print("==> WDT reload OK")
		else :
			_print_error_message("LMB_WDT_Tick", iRet)



	lib.LMB_DLL_DeInit()
	return iRet
if __name__ == '__main__':
	wdt_util()


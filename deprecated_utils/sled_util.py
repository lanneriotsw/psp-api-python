                                                                                                                   

from __future__ import print_function
import time
from ctypes import *
import sys,os
#import library
#--------------------------------------------------------------------#

cdll.LoadLibrary("/usr/local/lib/liblmbio.so")  
lib=cdll.LoadLibrary("/usr/local/lib/liblmbapi.so")


#--------------------------------------------------------------------#
def _err_print(pbString):

	print("\033[1;31m {:s} \033[0m".format(pbString)) 
#--------------------------------------------------------------------#

def __print_usage(argv0):

	print("Usage: %s -green/-red/-off  [-blink 16/8/4/2/1/0.5]\n\t--> setting System/Status LED".format(argv0))
	print("       %s -test [seconds]	\n\t--> for testing (default 2 seconds delay)".format(argv0))

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

	print("\033[1;31m{:s} return error code = 0x{:08x}, ".format(pstrFunc, errcode&0xFFFFFFFF),end="")

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
#--------------------------------------------------------------------#

def sled_util():

	iRet,index,xi= 0,0,1
	bsel= 0
	argc=len(sys.argv)
	dwDelay=2
	ubRead=c_uint8(0xFF)
	ubBlink=0xFF

	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 
	if  argc < 2  :
		__print_usage(sys.argv[0])
		return -1
	
	while  xi < argc :

		if "-green" == sys.argv[xi] : 
			bsel = 1
			xi += 1
		elif "-red" == sys.argv[xi] : 
			bsel = 2
			xi += 1
		elif "-off" == sys.argv[xi] :
			bsel = 0
			xi += 1
		elif "-blink" == sys.argv[xi] :
			if xi == argc-1 :
				print("<Warning> not input Blink setting (range 1 ~ 7)")
				return -1
			ftime=string.atof(sys.argv[xi+1])
			if ftime*10 == 160 :
				ubBlink = 1 #LED_BLINK_16S
			elif ftime*10 == 80 :
				ubBlink = 2 #LED_BLINK_8S
			elif ftime*10 == 40 :
				ubBlink = 3 #LED_BLINK_4S
			elif ftime*10 == 20 :
				ubBlink = 4 #LED_BLINK_2S
			elif ftime*10 == 10 :
				ubBlink = 5 #LED_BLINK_1S
			elif ftime*10 == 5 :
				ubBlink = 6 #LED_BLINK_HalfS
			xi += 2
		elif "-test" == sys.argv[xi] :
			bsel = 3
			if xi != argc-1 :
				dwDelay = int(sys.argv[xi+1])
				xi += 1
			xi += 1
		else :
			print("<Error> Input parameter invaild ")
			__print_usage(sys.argv[0])
			return -1

	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 
#	print(bsel)
	if (bsel == 0 or bsel == 1 or bsel == 2):
		if ubBlink == 0xFF :
			iRet = lib.LMB_SLED_SetSystemLED(bsel)
			if iRet != ERR_Success :
				print(iRet)
			iRet = lib.LMB_SLED_GetSystemLED(byref(ubRead))
			if iRet != ERR_Success :
				print(iRet)
			if bsel == ubRead.value :
				print("Status LED setting OK")
			else :
				print("\033[1;31m<Warning> Status LED setting failure\033[m")


		else :
			iRet = lib.LMB_SLED_SetSystemLED_Ex(bsel, ubBlink)
			if iRet != ERR_Success :
				_print_error_message("<ALARM> LMB_SLED_SetSystemLED_Ex", iRet)
				return -1
	if bsel == 3 :
		#//=========set LED green=======================//
		iRet = lib.LMB_SLED_SetSystemLED(1)
		if ( iRet != ERR_Success ) :
			 _print_error_message("<ALARM> LMB_SLED_SetSystemLED", iRet) 
		else :
			print("--> Set LED is Green")
	
		_show_delay(dwDelay)
		#//=========set LED red========================//
		iRet = lib.LMB_SLED_SetSystemLED(2)
		if ( iRet != ERR_Success ) :
			 _print_error_message("<ALARM> LMB_SLED_SetSystemLED", iRet) 
		else :
			print("--> Set LED is Red")
	
		_show_delay(dwDelay)
		#//========set lED off=====================//
		iRet = lib.LMB_SLED_SetSystemLED(0)
		if ( iRet != ERR_Success ) :
			 _print_error_message("<ALARM> LMB_SLED_SetSystemLED", iRet) 
		else :
			print("--> Set LED is Off")


	lib.LMB_DLL_DeInit()
	return iRet
if __name__ == '__main__':
	sled_util()



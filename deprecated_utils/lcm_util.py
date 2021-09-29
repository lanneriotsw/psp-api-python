                                                                                                                   

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

	print("Usage: {:s} -search						\n\t--> search LCM port and baudrate".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -reset 			\n\t--> reset LCD module".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -clear 			\n\t--> clear LCD module screen".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -startup \"startup message\"	\n\t--> setting LCM startup message after reset".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -light 0/1			\n\t--> control LCM backlight Off/On".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -wrap 0/1			\n\t--> control LCM line wrap Off/On".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -bright 0/../8		\n\t--> control LCM brightness".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -curtype 0/1/2		\n\t--> setting cussor type off/underline/block_blink".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -cursor #row [#column]	\n\t--> set cursor position".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -write \"string\"		\n\t--> write string to LCM".format(argv0))
	print("       {:s} [-port #dec] [-baud #dec] -setspeed #dec		\n\t--> setting new LCM connection speed".format(argv0))
	print("       {:s} -callback						\n\t--> Callback for LCM key button".format(argv0))
	print("Note: If not assigned port and speed, default is {:s} and {:d}".format(DEFAULT_LCMPORT, DEFAULT_BAUDRATE))


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
class INTRUSION_TIME(Structure):
	_fields_=[("uwYear",c_uint16),("ubMonth",c_uint8),("ubDay",c_uint8),("ubHour",c_uint8),("ubMinute",c_uint8),("ubSecond",c_uint8)]

class LCM_INFO(Structure):
	_fields_=[("uwModeNo",c_uint16),("uwVersion",c_uint16),("udwBaudrate",c_uint32)]

class LCMKEY_MSG(Structure):
	_fields_=[("ubKeys",c_uint8),("ubStatus",c_uint8),("stuTime",INTRUSION_TIME)]

c_callback=CFUNCTYPE(None,LCMKEY_MSG)
def LcmCallback(stuLcmMsg) :
	count = 1
	print("<Callback> LCM Item = 0x{:02X}, Status = 0x{:02X}, time is {:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(stuLcmMsg.ubKeys, stuLcmMsg.ubStatus, stuLcmMsg.stuTime.uwYear, stuLcmMsg.stuTime.ubMonth, stuLcmMsg.stuTime.ubDay,stuLcmMsg.stuTime.ubHour, stuLcmMsg.stuTime.ubMinute, stuLcmMsg.stuTime.ubSecond))

p_callback=c_callback(LcmCallback)
#--------------------------------------------------------------------#

LCM_UART_TYPE	=1
LCM_LPT_TYPE	=2

SEL_READ	=1
SEL_WRITE	=2
SEL_READ_PIN	=3
SEL_WRITE_PIN	=4

SEL_GPO		=1
SEL_GPI		=2
SEL_DATA	=1

DEFAULT_LCMPORT	="/dev/ttyS1"
DEFAULT_BAUDRATE=19200

CMD_RESET	=1
CMD_STARTUP	=2
CMD_LIGHT	=3
CMD_CURSOR	=4
CMD_WRITE	=5
CMD_SEARCH	=6
CMD_BRIGHT	=7
CMD_CLEAR	=8
CMD_WRAP	=9
CMD_CURTYPE	=10
CMD_CALLBACK	=11
CMD_SETSPEED	=12

ERR_Success	=0

#--------------------------------------------------------------------#

def lcm_util():

	iRet,index,xi= 0,0,1
	argc=len(sys.argv)
	LcmInfo=LCM_INFO()
	iLcmType = LCM_UART_TYPE
	iCmd = -1
	iRow,iCol=0,1
	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 
	strLcmPort = DEFAULT_LCMPORT
	dwSpeed = DEFAULT_BAUDRATE
	if  argc < 2  :
		__print_usage(sys.argv[0])
		return -1

	while  xi < argc :
		if "-reset" == sys.argv[xi] : 
			iCmd = CMD_RESET
			xi += 1
		elif "-port" == sys.argv[xi] : 
			if  xi == argc-1  :
				 print("<Warning> not input port")
				 return -1
			if "/dev/ttyS" in sys.argv[xi+1] :
				strLcmPort = sys.argv[xi+1]
			else :
				strLcmPort = "/dev/ttyS{:d}".format(int(sys.argv[xi+1]))
			xi += 2
		elif "-baud" == sys.argv[xi] :
			if  xi == argc-1  :
				 print("<Warning> not input baudrate")
				 return -1
			dwSpeed = int(sys.argv[xi+1])
			xi += 2
		elif "-search" == sys.argv[xi] : 
			iCmd = CMD_SEARCH
			xi += 1
		elif "-clear" == sys.argv[xi] : 
			iCmd = CMD_CLEAR
			xi += 1
		elif "-callback" == sys.argv[xi] : 
			iCmd = CMD_CALLBACK
			xi += 1
		elif "-startup" == sys.argv[xi] : 
			iCmd = CMD_STARTUP
			if  xi == argc-1  :
				 print("<Warning> not input string")
				 return -1
			strMsg = sys.argv[xi+1]
			xi += 2
		elif "-light" == sys.argv[xi] : 
			iCmd = CMD_LIGHT
			if  xi == argc-1  :
				 print("<Warning> not input 0/1")
				 return -1
			dwData = int(sys.argv[xi+1])
			if  dwData !=0 and dwData != 1 : 
				print("\033[1;31m<Warning> input out of range (0~1)\033[m") 
				return -1
			xi += 2
		elif "-setspeed" == sys.argv[xi] : 
			iCmd = CMD_SETSPEED
			if  xi == argc-1  :
				 print("<Warning> not input new speed")
				 return -1
			dwData = int(sys.argv[xi+1])
			if  dwData != 115200 and dwData != 57600 and dwData != 38400  and dwData != 19200 and dwData != 9600 : 
				print("\033[1;31m<Warning> is invlaid (115200/57600/38400/19200/9600\033[m") 
				return -1
			xi += 2
		elif "-curtype" == sys.argv[xi] : 
			iCmd = CMD_CURTYPE
			if  xi == argc-1  :
				 print("<Warning> not input 0/1/2")
				 return -1
			dwData = int(sys.argv[xi+1])
			if  dwData <0  or  dwData >2 : 
				print("\033[1;31m<Warning> input out of range (0~2)\033[m") 
				return -1
			xi += 2
		elif "-wrap" == sys.argv[xi] : 
			iCmd = CMD_WRAP
			if  xi == argc-1  :
				 print("<Warning> not input 0/1")
				 return -1
			dwData = int(sys.argv[xi+1])
			if  dwData !=0  and  dwData != 1 : 
				print("\033[1;31m<Warning> input out of range (0~1)\033[m") 
				return -1
			xi += 2
		elif "-bright" == sys.argv[xi] : 
			iCmd = CMD_BRIGHT
			if  xi == argc-1  :
				 print("<Warning> not input brightness 0~8")
				 return -1
			dwData = int(sys.argv[xi+1])
			if  dwData <0   or  dwData > 8 : 
				print("\033[1;31m<Warning> input out of range (0~8)\033[m") 
				return -1
			xi += 2
		elif "-cursor" == sys.argv[xi] : 
			iCmd = CMD_CURSOR
			if  xi == argc-1  :
				 print("<Warning>  not input #row and #column")
				 return -1
			iRow = int(sys.argv[xi+1])
			if  iRow !=1 and iRow != 2 : 
				print("\033[1;31m<Warning> input out of range (1~2)\033[m") 
				return -1
			xi += 1
			if xi == argc-1 :
				print("<Warning> not input #column, dfault 1")
			else :
				iCol = atoi(argv[xi+1])
				xi += 1
			xi += 1
		elif "-write" == sys.argv[xi] : 
			iCmd = CMD_WRITE
			if  xi == argc-1  :
				 print("<Warning> not input string")
				 return -1
			strMsg = sys.argv[xi+1]
			xi += 2
		else :
			__print_usage(sys.argv[0])
			return -1
	if iCmd == -1:
		__print_usage(sys.argv[0])
		return -1

	iRet = lib.LMB_DLL_Init()
	if iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet)
		return -1
	if iCmd != CMD_SEARCH:
		print("Open LCM port {:s}, speed={:d} ......".format(strLcmPort, dwSpeed),end='')
		iRet =lib.LMB_LCM_OpenPort(strLcmPort, dwSpeed)
		if ( iRet != ERR_Success ) :
			print("")
			_print_error_message("LMB_LCM_OpenPort", iRet) 
			return -1
		else :
			print("OK")
	iRet = lib.LMB_LCM_DeviceInfo(byref(LcmInfo))
	if ( iRet == ERR_Success ) :
		iLcmType = LCM_UART_TYPE
	else  :
		iLcmType = LCM_LPT_TYPE
	if iCmd == CMD_RESET :
		if iLcmType == LCM_UART_TYPE :
			iRet = lib.LMB_LCM_Reset()
			if iRet == ERR_Success :
				print("-->LMB_LCM_Reset OK ")
			else :
				_print_error_message("LMB_LCM_Reset", iRet)
		else :
			print("\033[1;34m--> LPT type not support reset\033[m")
	elif iCmd == CMD_SEARCH :
		dwSpeed=c_int32(dwSpeed)
		iRet = lib.LMB_LCM_SearchPort(strLcmPort, byref(dwSpeed))
		if iRet == ERR_Success :
			print("--> LMB_LCM_SearchPort OK, port={:s}, speed={:d} ".format(strLcmPort, dwSpeed.value))
		else :
			_print_error_message("LMB_LCM_SearchPort", iRet)
	elif iCmd == CMD_STARTUP :
		iRet = lib.LMB_LCM_StartupMsg(strMsg,len(strMsg))
		if iRet == ERR_Success :
			print("-->LMB_LCM_StartupMsg OK")
		else :
			_print_error_message("LMB_LCM_StartupMsg", iRet)
	elif iCmd == CMD_LIGHT :
		iRet = lib.LMB_LCM_LightCtrl(dwData&0xFF)
		if iRet == ERR_Success :
			print("--> LMB_LCM_LightCtrl OK")
		else :
			_print_error_message("LMB_LCM_LightCtrl", iRet)
	elif iCmd == CMD_CURSOR :
		iRet = lib.LMB_LCM_SetCursor(iCol, iRow)
		if iRet == ERR_Success :
			print("--> LMB_LCM_SetCursor Row,Column=%d,%d OK".format(iRow, iCol))
		else :
			_print_error_message("LMB_LCM_SetCursor", iRet)
	elif iCmd == CMD_WRITE :
		iRet = lib.LMB_LCM_WriteString(strMsg)
		if iRet == ERR_Success :
			print("--> LMB_LCM_WriteString display OK")
		else :
			_print_error_message("LMB_LCM_WriteString", iRet)
	elif iCmd ==  CMD_BRIGHT:
		if  iLcmType == LCM_UART_TYPE  :
			iRet = lib.LMB_LCM_Brightness((dwData&0xFF))
			if  iRet == ERR_Success  :
				print("--> LMB_LCM_Brightness OK ")
			else	:
				_print_error_message("LMB_LCM_Brightness", iRet)
		
		else :
			print("\033[1;34m--> LPT type not support brightness\033[m")
		
	elif iCmd ==  CMD_CLEAR:
		iRet = lib.LMB_LCM_DisplayClear()
		if  iRet == ERR_Success  :
			print("--> LMB_LCM_DisplayClear OK ") 
		else  	:
			_print_error_message("LMB_LCM_DisplayClear", iRet)
	elif iCmd ==  CMD_WRAP:
		if  iLcmType == LCM_UART_TYPE  :
			iRet = lib.LMB_LCM_WrapCtrl(dwData&0xFF)
			if  iRet == ERR_Success  :
				print("--> LMB_LCM_WrapCtrl OK ") 
			else  	: 
				_print_error_message("LMB_LCM_WrapCtrl", iRet)
		
		else 	 :
			print("\033[1;34m--> LPT type not support wrap control\033[m")

	elif iCmd ==  CMD_CURTYPE:
		if  iLcmType == LCM_UART_TYPE  :
			iRet = lib.LMB_LCM_CursorModeCtrl(dwData&0xFF)
			if  iRet == ERR_Success  :
				print("--> LMB_LCM_CursorModeCtrl OK ")
			else  	:
				_print_error_message("LMB_LCM_CursorModeCtrl", iRet)
		
		else 	:
			print("\033[1;34m--> LPT type not support cursor type control\033[m") 
	elif iCmd ==  CMD_CALLBACK:
		iRet = lib.LMB_LCM_KeysCallback(p_callback, 150)
		if  iRet == ERR_Success  :
			print("----> hook LCM Keys Callback OK <----") 
		else  	:
			print("-----> hook LCM Keys callback failure <-------")
			return -1
		print("===> pause !!! hit <enter> to end <===")
		sys.stdin.read(1)
		iRet = lib.LMB_LCM_KeysCallback(None, 150)
		if   iRet == ERR_Success  :
			print("----> hook LCM Keys Callback Disable OK <----")
	elif iCmd ==  CMD_SETSPEED:
		if  iLcmType == LCM_UART_TYPE  :
			iRet = lib.LMB_LCM_SetSpeed(dwData)
			if  iRet == ERR_Success  :
				print("--> LMB_LCM_SetSpeed OK ")
			else  	:
				_print_error_message("LMB_LCM_SetSpeed", iRet)
		
		else 	:
			print("\033[1;34m--> LPT type not support speed setting\033[m") 
	else :
		__print_usage(sys.argv[0])
		return -1
		


	lib.LMB_LCM_DeviceClose()

	lib.LMB_DLL_DeInit()
	return iRet

#--------------------------------------------------------------------#
if __name__ == '__main__':
	lcm_util()



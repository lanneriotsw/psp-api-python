
from __future__ import print_function
import time
from ctypes import *
import sys,os




#import library
#--------------------------------------------------------------------#

cdll.LoadLibrary("/usr/local/lib/liblmbio.so")  
lib=cdll.LoadLibrary("/usr/local/lib/liblmbapi.so")

#--------------------------------------------------------------------#
#--------------------------------------------------------------------#

class IPMI_SENSOR_INFO(Structure):
	_fields_=[("strName",c_int8*16),("fValue",c_float),("fHiCritcal",c_float),("fLoCritcal",c_float),("strUnit",c_int8*16)]

class IPMI_SDRMAP(Structure):
	_fields_=[("uwIdNum",c_uint16),("strName",c_int8*16),("ubKcsReg",c_uint8)]

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
def _err_print(pbString):

	print("\033[1;31m {:s} \033[0m".format(pbString)) 
#--------------------------------------------------------------------#
#--------------------------------------------------------------------#
def ipmi_python():
	ipmi_extime=[0]*10
	iRet,ERR_Success= 0,0
	index,xloop,spaceLen = 0 ,0 ,0
	ftemp=c_float()
	dwData=c_uint32()
	dwCount=c_int32()
	stuSensorInfo=IPMI_SENSOR_INFO()
	sdPtr=IPMI_SDRMAP()
	aryData=create_string_buffer(sizeof(IPMI_SDRMAP)*256)



	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 
	
	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		#//_printf_error_message("LMB_DLL_Init", iret) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 

	print(".....IPMI....................")
	for xloop in range(1):
		index =0 	
		#LMB_IPMI_BmcVersion

		iRet = lib.LMB_IPMI_BmcVersion(byref(dwData))

		if iRet ==  ERR_Success : 
			print("LMB_IPMI_BmcVersion = {:d}".foramt(dwData.value))
		else :
			_print_error_message("LMB_IPMI_BmcVersion", iRet)

		index += 1 

		#LMB_IPMI_GetIDs

		iRet = lib.LMB_IPMI_GetIDs(aryData, byref(dwCount))

		if iRet ==  ERR_Success : 
			print("LMB_IPMI_GetIDs = {:d}".foramt(dwCount.value))
		else :
			_print_error_message("LMB_IPMI_GetIDs", iRet)
		index += 1 


		#LMB_IPMI_InfoByName

		iRet = lib.LMB_IPMI_InfoByName(sdPtr.strName, byref(stuSensorInfo))

		if iRet ==  ERR_Success : 
			print("LMB_IPMI_InfoByName = {:d}".foramt(stuSensorInfo.value))
		else :
			_print_error_message("LMB_IPMI_InfoByName", iRet)	
		index += 1 


		#LMB_IPMI_InfoByRecID

		iRet = lib.LMB_IPMI_InfoByRecID(sdPtr.uwIdNum, byref(stuSensorInfo))

		if iRet ==  ERR_Success : 
			print("LMB_IPMI_InfoByRecID = {:d}".foramt(stuSensorInfo.value))
		else :
			_print_error_message("LMB_IPMI_InfoByRecID", iRet)	
		index += 1 


		#LMB_IPMI_InfoByNum

		iRet = lib.LMB_IPMI_InfoByNum(sdPtr.ubKcsReg, byref(stuSensorInfo))

		if iRet ==  ERR_Success : 
			print("LMB_IPMI_InfoByNum = {:d}".foramt(stuSensorInfo.value))
		else :
			_print_error_message("LMB_IPMI_InfoByNum", iRet)
		index += 1 

		itemCnt = index  

if __name__ == '__main__':
	ipmi_python()

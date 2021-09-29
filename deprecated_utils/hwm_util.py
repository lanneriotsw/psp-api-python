                                                                                                                   

from __future__ import print_function
import time
from ctypes import *
import sys,os,string
import struct

#import library
#--------------------------------------------------------------------#

cdll.LoadLibrary("/usr/local/lib/liblmbio.so")  
lib=cdll.LoadLibrary("/usr/local/lib/liblmbapi.so")
lib2=cdll.LoadLibrary("./libcommon.so")

#--------------------------------------------------------------------#
def _err_print(pbString):

	print("\033[1;31m {:s} \033[0m".format(pbString)) 
#--------------------------------------------------------------------#

def __print_usage(argv0):

	print("Usage: {:s} -temp cpu1/cpu2/sys1/sys2".format(argv0))
	print("       {:s} -volt core1/core2/12v/5v/3v3/5vsb/3v3sb/vbat/psu1/psu2".format(argv0))
	print("       {:s} -rpm fan1/fan2/fan3/..../fan10".format(argv0))
#if SUPPORT_FAN_AB
	if SUPPORT_FAN_AB :
		print("       {:s} -rpm fan1a/fan1b/fan2a/fan2b/....../fan10a/fan10b".format(argv0))
#endif
	print("       {:s} -callback		--> uses callback detect caseopen".format(argv0))
	print("       {:s} -sidname #dec	--> print sensor name by #dec".format(argv0))	
	print("       {:s} -sidmsg #dec		--> print sensor message by #dec".format(argv0)) 
	print("       {:s} -sidlist 		--> print list all supports sensor ID".format(argv0))
	print("       {:s} -testop [seconds]	--> for caseopen testing (default:5)".format(argv0))
	print("       {:s} -testhwm [-c file]	--> for testing(default:hwm.conf)".format(argv0)) 


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

SUPPORT_FAN_AB	=1
ALARM		="\033[1;31mALARM\033[m"

FAN_A		=1
FAN_B		=2

ITEM_TEMP	=1
ITEM_VOLT	=2
ITEM_RPM	=3
ITEM_CALLBACK	=4
ITEM_TESTOP	=5
ITEM_TESTHWM	=6
ITEM_SIDNAME	=7
ITEM_SIDMSG	=8
ITEM_SIDLIST	=9

HWM_TYPE_NONE	=0
HWM_TYPE_SIO	=1
HWM_TYPE_IPMI	=2
HWM_TYPE_SMBUS	=3
HWM_TYPE_AST1400=4

ERR_Success	=0
CONFIG_NAME= "hwm.conf"
dwSensorType = c_int32()
#--------------------------------------------------------------------#
def create_var_range(first_val, *names):
	for name in names:
		globals()[name] = first_val
		first_val += 1
create_var_range(0,
		#//Temperature area
		'HWMID_TEMP_CPU1',
		'HWMID_TEMP_CPU2',
		'HWMID_TEMP_SYS1',
		'HWMID_TEMP_SYS2',
		#//Voltage area
		'HWMID_VCORE_CPU1',
		'HWMID_VCORE_CPU2',
		'HWMID_VOLT_P12V',
		'HWMID_VOLT_P5V',
		'HWMID_VOLT_P3V3',
		'HWMID_VOLT_P5VSB',
		'HWMID_VOLT_P3V3SB',
		'HWMID_VOLT_VBAT',
		'HWMID_VOLT_DDRCH1',
		'HWMID_VOLT_DDRCH2',
		'HWMID_VOLT_DDRCH3',
		'HWMID_VOLT_DDRCH4',
		'HWMID_VOLT_DDRCH5',
		'HWMID_VOLT_DDRCH6',
		'HWMID_VOLT_DDRCH7',
		'HWMID_VOLT_DDRCH8',
		'HWMID_VOLT_PVNN',
		'HWIID_VOLT_P1V05',
		'HWMID_VOLT_PVCCIO_CPU1',
		'HWMID_VOLT_PVCCIO_CPU2',
		'HWMID_VOLT_PVCCSA_CPU1',
		'HWMID_VOLT_PVCCSA_CPU2',
		#//Fan area
		'HWMID_RPM_FanCpu1',
		'HWMID_RPM_FanCpu2',
		'HWMID_RPM_FanSys1',
		'HWMID_RPM_FanSys2',
		'HWMID_RPM_Fan1A',
		'HWMID_RPM_Fan1B',
		'HWMID_RPM_Fan2A',
		'HWMID_RPM_Fan2B',
		'HWMID_RPM_Fan3A',
		'HWMID_RPM_Fan3B',
		'HWMID_RPM_Fan4A',
		'HWMID_RPM_Fan4B',
		'HWMID_RPM_Fan5A',
		'HWMID_RPM_Fan5B',
		'HWMID_RPM_Fan6A',
		'HWMID_RPM_Fan6B',
		'HWMID_RPM_Fan7A',
		'HWMID_RPM_Fan7B',
		'HWMID_RPM_Fan8A',
		'HWMID_RPM_Fan8B',
		'HWMID_RPM_Fan9A',
		'HWMID_RPM_Fan9B',
		'HWMID_RPM_Fan10A',
		'HWMID_RPM_Fan10B',
		#//Power supply area
		'HWMID_PSU1_STATUS',
		'HWMID_PSU1_VOLTIN',
		'HWMID_PSU1_VOLTOUT',
		'HWMID_PSU1_CURRENTIN',
		'HWMID_PSU1_CURRENTOUT',
		'HWMID_PSU1_POWERIN',
		'HWMID_PSU1_POWEROUT',
		'HWMID_PSU1_FAN1',
		'HWMID_PSU1_FAN2',
		'HWMID_PSU1_TEMP1',
		'HWMID_PSU1_TEMP2',
		'HWMID_PSU2_STATUS',
		'HWMID_PSU2_VOLTIN',
		'HWMID_PSU2_VOLTOUT',
		'HWMID_PSU2_CURRENTIN',
		'HWMID_PSU2_CURRENTOUT',
		'HWMID_PSU2_POWERIN',
		'HWMID_PSU2_POWEROUT',
		'HWMID_PSU2_FAN1',
		'HWMID_PSU2_FAN2',
		'HWMID_PSU2_TEMP1',
		'HWMID_PSU2_TEMP2',
		#//add here for new items
		#//
		'HWMID_TOTAL')
wtime = 5
#--------------------------------------------------------------------#
def _test_caseopen() :
	ubRead=c_uint8(0)
	dwCnt =0
	index=wtime
	itime=index
	iRet = lib.LMB_HWM_ClearCaseOpenStatus()
	if iRet != ERR_Success :
		_print_error_message("LMB_HWM_ClearCaseOpenStatus", iRet)
		return
	print("===> wait {:d} seconds for CaseOpen Detection .......".format(itime))
	ubRead=c_uint8(0)
	while (1) :
		if dwCnt % 10 == 0 :
			print("{:d}. ".format(index),end='')
			index -= 1
			sys.stdout.flush()
		dwCnt += 1
		if dwCnt > itime*10 :
			break
		time.sleep(0.1)
		lib.LMB_HWM_CaseOpenStatus(byref(ubRead))
		if ubRead :
			break
	print("")
	if ubRead.value == 1:
		print("CaseOpen detection --> OK")
	else:
		print("\033[1;31mCaseOpen not deteced ! --> ALARM\033[0m")
	time.sleep(0.1)
	lib.LMB_HWM_ClearCaseOpenStatus()

#--------------------------------------------------------------------#
def  __calc_space_string(pbStr):

	spaceLen=0
	spaceLen = 16-len(pbStr)
	return spaceLen
#--------------------------------------------------------------------#

def hwm_util():

	iRet,index,xi= 0,0,1
	argc=len(sys.argv)
	wsub,spaceLen =0,0
	wrpm=c_uint16()
	ftemp=c_float()
	wData=c_uint16()
	strMsg,strMsg2,strMsg3 = create_string_buffer(50),create_string_buffer(50),create_string_buffer(50)
	strSpace =((c_char *31)*2)()
	global CONFIG_NAME

	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 

	if  argc < 2  :
		__print_usage(sys.argv[0])
		return -1
	while  xi < argc :
		if "-temp" == sys.argv[xi] :
			bsel = ITEM_TEMP
			if xi == argc-1:
				_err_print("<Warning> not input item name")
				return -1
			if "cpu1" == sys.argv[xi+1] :
				wsub = 101
			elif "cpu2" == sys.argv[xi+1] :
				wsub = 102
			elif "sys1" == sys.argv[xi+1] :
				wsub = 103
			elif "sys2" == sys.argv[xi+1] :
				wsub = 104
			else :
				_err_print("<Error> Input parameter invaild")
				__print_usage(sys.argv[0])
				return -1
			xi += 2
		elif "-volt" == sys.argv[xi] :
			bsel = ITEM_VOLT
			if xi == argc-1:
				_err_print("<Warning> not input item name")
				return -1
			if "core1" == sys.argv[xi+1] :
				wsub = 201
			elif "core2" == sys.argv[xi+1] :
				wsub = 202
			elif "12v" == sys.argv[xi+1] :
				wsub = 203
			elif "5v" == sys.argv[xi+1] :
				wsub = 204
			elif "3v3" == sys.argv[xi+1] :
				wsub = 205
			elif "5vsb" == sys.argv[xi+1] :
				wsub = 206
			elif "3v3sb" == sys.argv[xi+1] :
				wsub = 207
			elif "vbat" == sys.argv[xi+1] :
				wsub = 208
			elif "psu1" == sys.argv[xi+1] :
				wsub = 209
			elif "psu2" == sys.argv[xi+1] :
				wsub = 210
			else :
				_err_print("<Error> Input parameter invaild")
				__print_usage(sys.argv[0])
				return -1
			xi += 2
		elif "-rpm" == sys.argv[xi] :
			bsel = ITEM_RPM
			if xi == argc-1:
				_err_print("<Warning> not input item name")
				return -1
			if "fan1" == sys.argv[xi+1] :
				wsub = 301
			elif "fan2" == sys.argv[xi+1] :
				wsub = 302
			elif "fan3" == sys.argv[xi+1] :
				wsub = 303
			elif "fan4" == sys.argv[xi+1] :
				wsub = 304
			elif "fan5" == sys.argv[xi+1] :
				wsub = 305
			elif "fan6" == sys.argv[xi+1] :
				wsub = 306
			elif "fan7" == sys.argv[xi+1] :
				wsub = 307
			elif "fan8" == sys.argv[xi+1] :
				wsub = 308
			elif "fan9" == sys.argv[xi+1] :
				wsub = 309
			elif "fan10" == sys.argv[xi+1] :
				wsub = 310
			if SUPPORT_FAN_AB:
				if "fan1a" == sys.argv[xi+1] :
					wsub = 401
				elif "fan1b" == sys.argv[xi+1] :
					wsub = 402
				elif "fan2a" == sys.argv[xi+1] :
					wsub = 403
				elif "fan2b" == sys.argv[xi+1] :
					wsub = 404
				elif "fan3a" == sys.argv[xi+1] :
					wsub = 405
				elif "fan3b" == sys.argv[xi+1] :
					wsub = 406
				elif "fan4a" == sys.argv[xi+1] :
					wsub = 407
				elif "fan4b" == sys.argv[xi+1] :
					wsub = 408
				elif "fan5a" == sys.argv[xi+1] :
					wsub = 409
				elif "fan5b" == sys.argv[xi+1] :
					wsub = 410
				elif "fan6a" == sys.argv[xi+1] :
					wsub = 411
				elif "fan6b" == sys.argv[xi+1] :
					wsub = 412
				elif "fan7a" == sys.argv[xi+1] :
					wsub = 413
				elif "fan7b" == sys.argv[xi+1] :
					wsub = 414
				elif "fan8a" == sys.argv[xi+1] :
					wsub = 415
				elif "fan8b" == sys.argv[xi+1] :
					wsub = 416
				elif "fan9a" == sys.argv[xi+1] :
					wsub = 417
				elif "fan9b" == sys.argv[xi+1] :
					wsub = 418
				elif "fan10a" == sys.argv[xi+1] :
					wsub = 419
				elif "fan10b" == sys.argv[xi+1] :
					wsub = 420
				else:
					_err_print("<Error> Input parameter invaild")
					__print_usage(sys.argv[0])
					return -1
			elif wsub==0 and SUPPORT_FAN_AB ==0:
				_err_print("<Error> Input parameter invaild")
				__print_usage(sys.argv[0])
				return -1
			xi += 2
		elif "-callback" == sys.argv[xi] :
			bsel = ITEM_CALLBACK
			xi += 1
		elif "-testop" == sys.argv[xi] :
			bsel = ITEM_TESTOP
			if xi < argc-1 :
				wtime = int(argv[xi+1]) 
				xi+=1
			xi+=1
		elif "-testhwm" == sys.argv[xi] :
			bsel = ITEM_TESTHWM
			xi += 1
		elif "-sidname" == sys.argv[xi] :
			bsel = ITEM_SIDNAME
			if xi == argc-1 :
				_err_print("<Warning> not input sensor ID number") 
				return -1
			sid = int(sys.argv[xi+1])
			xi += 2
		elif "-sidmsg" == sys.argv[xi] :
			bsel = ITEM_SIDMSG
			if xi == argc-1 :
				_err_print("<Warning> not input sensor ID number") 
				return -1
			sid = int(sys.argv[xi+1])
			xi += 2
		elif "-sidlist" == sys.argv[xi] :
			bsel = ITEM_SIDLIST
			xi += 1
		elif "-c" == sys.argv[xi] :

			if xi == argc-1 :
				_err_print("<Warning> not input file name") 
				return -1
			if xi < argc:
				CONFIG_NAME=sys.argv[xi]
			xi += 1
		else :
			__print_usage(sys.argv[0])
			return -1
#	/***************************************/
	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 

	if bsel == ITEM_TEMP:
		if wsub == 101:
			iRet = lib.LMB_HWM_GetCpuTemp(1, byref(ftemp))
			if iRet == ERR_Success:
				print("CPU-1 temperature = {:.0f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_GetCpuTemp", iRet)
		elif wsub == 102:
			iRet = lib.LMB_HWM_GetCpuTemp(2, byref(ftemp))
			if iRet == ERR_Success:
				print("CPU-2 temperature = {:.0f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_GetCpuTemp", iRet)
		elif wsub == 103:
			iRet = lib.LMB_HWM_GetSysTemp(1, byref(ftemp))
			if iRet == ERR_Success:
				print("SYS-1 temperature = {:.0f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_GetSysTemp", iRet)
		elif wsub == 104:
			iRet = lib.LMB_HWM_GetSysTemp(2, byref(ftemp))
			if iRet == ERR_Success:
				print("SYS-2 temperature = {:.0f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_GetSysTemp", iRet)
		else:
			print("<Error> Input parameter invaild ")
			__print_usage(sys.argv[0])
			return -1
	elif bsel == ITEM_VOLT:
		if wsub == 201:
			iRet = lib.LMB_HWM_GetVcore(1, byref(ftemp))
			if iRet == ERR_Success:
				print("CPU-1 Vcore = {:2.3f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_GetVcore", iRet)
		elif wsub == 202:
			iRet = lib.LMB_HWM_GetVcore(2, byref(ftemp))
			if iRet == ERR_Success:
				print("CPU-1 Vcore = {:2.3f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_GetVcore", iRet)
		elif wsub == 203:
			iRet = lib.LMB_HWM_Get12V(byref(ftemp))
			if iRet == ERR_Success:
				print("12V = {:2.3f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_Get12V", iRet)
		elif wsub == 204:
			iRet = lib.LMB_HWM_Get5V(byref(ftemp))
			if iRet == ERR_Success:
				print("5V = {:2.3f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_Get5V", iRet)
		elif wsub == 205:
			iRet = lib.LMB_HWM_Get3V3(byref(ftemp))
			if iRet == ERR_Success:
				print("3.3V = {:2.3f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_Get3V3", iRet)
		elif wsub == 206:
			iRet = lib.LMB_HWM_Get5Vsb(byref(ftemp))
			if iRet == ERR_Success:
				print("5VSB = {:2.3f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_Get5Vsb", iRet)
		elif wsub == 207:
			iRet = lib.LMB_HWM_Get3V3sb(byref(ftemp))
			if iRet == ERR_Success:
				print("3.3VSB = {:2.3f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_Get3V3sb", iRet)
		elif wsub == 208:
			iRet = lib.LMB_HWM_GetVbat(2, byref(ftemp))
			if iRet == ERR_Success:
				print("Vbat = {:2.3f}".format(ftemp.value))
			else:
				_print_error_message("LMB_HWM_GetVbat", iRet)
		elif wsub == 209:
			iRet = lib.LMB_HWM_GetPowerSupply(1, byref(wData))
			if iRet == ERR_Success:
				print("PowerSupply 1 AC voltage = {:d}".format(wData.value))
			else:
				_print_error_message("LMB_HWM_GetVcore", iRet)
		elif wsub == 210:
			iRet = lib.LMB_HWM_GetPowerSupply(2, byref(wData))
			if iRet == ERR_Success:
				print("PowerSupply 2 AC voltage = {:d}".format(wData.value))
			else:
				_print_error_message("LMB_HWM_GetVcore", iRet)
		else:
			print("<Error> Input parameter invaild ")
			__print_usage(sys.argv[0])
			return -1
	elif bsel == ITEM_RPM:
		if 301 <= wsub <= 310 :
			iRet = lib.LMB_HWM_GetFanSpeed(wsub-300, byref(wrpm))
			if  iRet == ERR_Success  :
				print("FAN {:d} speed = {:d}".format(wsub-300, wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 401 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(1, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 1A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 402 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(1, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 1B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 403 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(2, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 2A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 404 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(2, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 2B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 405 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(3, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 3A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 406 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(3, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 3B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 407 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(4, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 4A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 408 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(4, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 4B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 409 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(5, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 5A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 410 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(5, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 5B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 411 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(6, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 6A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 412 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(6, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 6B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 413 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(7, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 7A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 414 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(7, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 7B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 415 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(8, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 8A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 416 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(8, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 8B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 417 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(9, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 9A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 418 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(9, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 9B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 419 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(108, byref(wrpm), FAN_A)
			if  iRet == ERR_Success  :
				print("FAN 10A speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
 		elif wsub == 420 :
			iRet = lib.LMB_HWM_GetFanSpeedEx(10, byref(wrpm), FAN_B)
			if  iRet == ERR_Success  :
				print("FAN 10B speed = {:d}".format(wrpm.value))
			else 	:	  	   
				_print_error_message("LMB_HWM_GetFanSpeed", iRet)
		else:
			print("<Error> Input parameter invaild ")
			__print_usage(sys.argv[0])
			return -1
	elif bsel == ITEM_CALLBACK:
		_exec_callback()
	elif bsel == ITEM_TESTOP:
		_test_caseopen()
	elif bsel == ITEM_SIDNAME:
		memset(strMsg, 0, 30)
		iRet = lib.LMB_HWM_GetSensorName(sid, strMsg)
		if  iRet == ERR_Success  :
			print("ID={:d}, name is \"{:s}\"".format(sid, strMsg.value))
		else 	:	  	   
			_print_error_message("LMB_HWM_GetSensorName", iRet)
	elif bsel == ITEM_SIDMSG:
		memset(strMsg, 0, 30)
		iRet = lib.LMB_HWM_GetSensorName(sid, strMsg2)
		if  iRet == ERR_Success  :
			spaceLen = 22-len(strMsg2)
		else 	:	  	   
			spaceLen = 22
		for xj in range(spaceLen) :
			strSpace[0][xj]=' '
		print("ID={:2d}(\"{:s}\"), ".format(sid, strMsg2.value),end='')
		iRet = lib.LMB_HWM_GetSensorReport(sid, strMsg)
		if ( iRet == ERR_Success ) :
			print("message=\"{:s}\"".format(strMsg.value))
		else 		  	   :
			_print_error_message("LMB_HWM_GetSensorName", iRet)
	elif bsel == ITEM_SIDLIST:

		for xxi in range(HWMID_TOTAL) :
			lib.LMB_HWM_GetSensorDisplay(xxi, strMsg3)
			spaceLen = 16-len(strMsg3.value)
			for xj in  range(spaceLen) : 
				strSpace[1][xj]=' '
			strSpace[1][spaceLen]=chr(0x00)
			iRet = lib.LMB_HWM_GetSensorReport(xxi, strMsg2)
			if  iRet == ERR_Success :
				memset(strMsg, 0, 50)
				iRet = lib.LMB_HWM_GetSensorName(xxi, strMsg)
				spaceLen2 = 22-len(strMsg.value)
				for xj in range (spaceLen) :
					strSpace[0][xj]=' '
				strSpace[0][spaceLen]=chr(0x00)
				if  iRet == ERR_Success  :
					print("ID={:2d}(\"{:s}\"),{:s} Name=\"{:s}\"{:s} {:s}".format(xxi, strMsg.value,strSpace[0].value,strMsg3.value,strSpace[1].value, strMsg2.value))
				else 		 : 	   
					_print_error_message("LMB_HWM_GetSensorName", iRet)
	elif bsel == ITEM_TESTHWM :
		_hwm_tst()

	else:
		__print_usage(sys.argv[0])


	lib.LMB_DLL_DeInit()
	return iRet

#--------------------------------------------------------------------#
def binaryToFloat(value):
	value=bin(value)[2:]
	hx = int(value,2)
	return struct.unpack("f",struct.pack("I",hx))[0]

def myAtoi(str):
	"""
	:type str: str
	:rtype: int
	"""
	import re
	
	pattern = r"[\s]*[+-]?[\d]+"
	match = re.match(pattern, str)
	if match:
		res = int(match.group(0))
		if res > 2 ** 31 - 1:
			res = 2 ** 31 -1
		if res < - 2 ** 31:
			res = - 2 ** 31
	else:
		res = 0
	return res

#--------------------------------------------------------------------#

def _show_temperature(sid):
	strMsg,strDisp,strIdName=create_string_buffer(30),create_string_buffer(30),create_string_buffer(30)
	min,max=0,0	
	udwLoCritical, udwHiCritical = c_uint32(),c_uint32()
	spaceLen=0
	fFlagValue = 0
	global dwSensorType , CONFIG_NAME

	memset(strMsg,0,30)
	if  lib.LMB_HWM_GetSensorReport(sid, strMsg) != -5  :
		lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
		lib.LMB_HWM_GetSensorName(sid, strIdName)
		min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))
		if min ==999999 :
			if dwSensorType == HWM_TYPE_IPMI:
				iRet = lib.LMB_IPMI_InfoByName(strDisp, byref(stuSensorInfo))
				if iRet == ERR_Success :
					min=stuSensorInfo.fLoCritcal
					max = stuSensorInfo.fHiCritcal
				else:
					min = max = 0
			else :
				lib.LMB_HWM_GetSensorCritical(sid , byref(udwLoCritical), byref(udwHiCritical))
				min = udwLoCritical.value / 1000
				max = udwHiCritical.value / 1000
		else :
			max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))
		if min == 99999 or min == 999999 :
			fFlagValue |= 0x01
		if max == 99999 or max == 999999 :
			fFlagValue |= 0x02
		spaceLen=__calc_space_string(strDisp.value)
		ftemp=myAtoi(strMsg.value)/1000
		if fFlagValue == 0x01:
			print("{:s}{:s} = {:7d} C\t(min = --N/A-- C, max = {:7d} C)".format(strDisp.value," "*spaceLen,ftemp,int(max)),end='')
			if ftemp > max :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x02:
			print("{:s}{:s} = {:7d} C\t(min = {:7d} C, max = --N/A-- C)".format(strDisp.value," "*spaceLen,ftemp,int(min)),end='')
			if ftemp < min :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x03:
			print("{:s}{:s} = {:7d} C\t(min = --N/A-- C, max = --N/A-- C)".format(strDisp.value," "*spaceLen,ftemp),end='')
		else:
			print("{:s}{:s} = {:7d} C\t(min = {:7d} C, max = {:7d} C)".format(strDisp.value," "*spaceLen,ftemp,min,max),end='')
			if ((ftemp < min) or (ftemp > max)) :
				print(" {:s}".format(ALARM),end='')
		print("")
	sys.stdout.flush()


#--------------------------------------------------------------------#

def _show_rpm(sid) :

	strMsg,strDisp,strIdName=create_string_buffer(30),create_string_buffer(30),create_string_buffer(30)
	min,max=0,0	
	udwLoCritical, udwHiCritical = c_uint32(),c_uint32()
	spaceLen=0
	fFlagValue = 0
	global dwSensorType , CONFIG_NAME

	memset(strMsg,0,30)
	if  lib.LMB_HWM_GetSensorReport(sid, strMsg) != -5  :
		lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
		lib.LMB_HWM_GetSensorName(sid, strIdName)
		min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))
		if min ==999999 :
			if dwSensorType == HWM_TYPE_IPMI:
				iRet = lib.LMB_IPMI_InfoByName(strDisp, byref(stuSensorInfo))
				if iRet == ERR_Success :
					min=stuSensorInfo.fLoCritcal
					max = stuSensorInfo.fHiCritcal
				else:
					min = max = 0
			else :
				lib.LMB_HWM_GetSensorCritical(sid , byref(udwLoCritical), byref(udwHiCritical))
				min = udwLoCritical.value
				max = udwHiCritical.value
		else :
			max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))
		if min == 99999 or min == 999999 :
			fFlagValue |= 0x01
		if max == 99999 or max == 999999 :
			fFlagValue |= 0x02
		spaceLen=__calc_space_string(strDisp.value)
		wrpm=myAtoi(strMsg.value)
		if fFlagValue == 0x01:
			print("{:s}{:s} = {:5d} rpm\t(min = --N/A-- rpm, max = {:5d} rpm)".format(strDisp.value," "*spaceLen,wrpm,int(max)),end='')
			if wrpm > max :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x02:
			print("{:s}{:s} = {:5d} rpm\t(min = {:5d} rpm, max = --N/A-- rpm)".format(strDisp.value," "*spaceLen,wrpm,int(min)),end='')
			if wrpm < min :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x03:
			print("{:s}{:s} = {:5d} rpm\t(min = --N/A-- rpm, max = --N/A-- rpm)".format(strDisp.value," "*spaceLen,wrpm),end='')
		else:
			print("{:s}{:s} = {:5d} rpm\t(min = {:5d} rpm, max = {:5d} rpm)".format(strDisp.value," "*spaceLen,wrpm,min,max),end='')
			if ((wrpm < min) or (wrpm > max)) :
				print(" {:s}".format(ALARM),end='')
		print("")
	sys.stdout.flush()
#--------------------------------------------------------------------#
def _show_voltage(sid):
	
	strMsg,strDisp,strIdName=create_string_buffer(30),create_string_buffer(30),create_string_buffer(30)
	min,max=0,0	
	udwLoCritical, udwHiCritical = c_uint32(),c_uint32()
	spaceLen=0
	fFlagValue = 0
	global dwSensorType , CONFIG_NAME

	memset(strMsg,0,30)
	if  lib.LMB_HWM_GetSensorReport(sid, strMsg) != -5  :
		lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
		lib.LMB_HWM_GetSensorName(sid, strIdName)
		min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))
		if min ==999999 :
			if dwSensorType == HWM_TYPE_IPMI:
				iRet = lib.LMB_IPMI_InfoByName(strDisp, byref(stuSensorInfo))
				if iRet == ERR_Success :
					min=stuSensorInfo.fLoCritcal
					max = stuSensorInfo.fHiCritcal
				else:
					min = max = 0
			else :
				lib.LMB_HWM_GetSensorCritical(sid , byref(udwLoCritical), byref(udwHiCritical))
				min = float(udwLoCritical.value) / float(1000)
				max = float(udwHiCritical.value) / float(1000)
		else :
			max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))
		if min == 99999 or min == 999999 :
			fFlagValue |= 0x01
		if max == 99999 or max == 999999 :
			fFlagValue |= 0x02
		spaceLen=__calc_space_string(strDisp.value)
		ftemp=float(myAtoi(strMsg.value)/float(1000))  
		RoundUp_buffer=ftemp*1000
		if fFlagValue == 0x01:
			print("{:s}{:s} = {:7.3f} V\t(min = --N/A-- V, max = {:7.3f} V)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,max),end='')
			if RoundUp_buffer > max*1000 :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x02:
			print("{:s}{:s} = {:7.3f} V\t(min = {:7.3f} V, max = --N/A-- V)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,min),end='')
			if RoundUp_buffer < min*1000 :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x03:
			print("{:s}{:s} = {:7.3f} V\t(min = --N/A-- V, max = --N/A-- V)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001),end='')
		else:
			print("{:s}{:s} = {:7.3f} V\t(min = {:7.3f} V, max = {:7.3f} V)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,min,max),end='')
			if ((RoundUp_buffer < min*1000) or (RoundUp_buffer > max*1000)) :
				print(" {:s}".format(ALARM),end='')
		print("")
	sys.stdout.flush()



#--------------------------------------------------------------------#
def _show_current(sid):
	
	strMsg,strDisp,strIdName=create_string_buffer(30),create_string_buffer(30),create_string_buffer(30)
	min,max=0,0	
	udwLoCritical, udwHiCritical = c_uint32(),c_uint32()
	spaceLen=0
	fFlagValue = 0
	global dwSensorType , CONFIG_NAME

	memset(strMsg,0,30)
	if  lib.LMB_HWM_GetSensorReport(sid, strMsg) != -5  :
		lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
		lib.LMB_HWM_GetSensorName(sid, strIdName)
		min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))
		if min ==999999 :
			if dwSensorType == HWM_TYPE_IPMI:
				iRet = lib.LMB_IPMI_InfoByName(strDisp, byref(stuSensorInfo))
				if iRet == ERR_Success :
					min=stuSensorInfo.fLoCritcal
					max = stuSensorInfo.fHiCritcal
				else:
					min = max = 0
			else :
				lib.LMB_HWM_GetSensorCritical(sid , byref(udwLoCritical), byref(udwHiCritical))
				min = float(udwLoCritical.value) / float(1000)
				max = float(udwHiCritical.value) / float(1000)
		else :
			max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))
		if min == 99999 or min == 999999 :
			fFlagValue |= 0x01
		if max == 99999 or max == 999999 :
			fFlagValue |= 0x02
		spaceLen=__calc_space_string(strDisp.value)
		ftemp=float(myAtoi(strMsg.value)/float(1000))  
		RoundUp_buffer=ftemp*1000
		if fFlagValue == 0x01:
			print("{:s}{:s} = {:7.3f} A\t(min = --N/A-- A, max = {:7.3f} A)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,max),end='')
			if RoundUp_buffer > max*1000:
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x02:
			print("{:s}{:s} = {:7.3f} A\t(min = {:7.3f} A, max = --N/A-- A)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,min),end='')
			if RoundUp_buffer < min*1000 :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x03:
			print("{:s}{:s} = {:7.3f} A\t(min = --N/A-- A, max = --N/A-- A)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001),end='')
		else:
			print("{:s}{:s} = {:7.3f} A\t(min = {:7.3f} A, max = {:7.3f} A)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,min,max),end='')
			if ((RoundUp_buffer < min*1000) or (RoundUp_buffer > max*1000)) :
				print(" {:s}".format(ALARM),end='')
		print("")
	sys.stdout.flush()



#--------------------------------------------------------------------#
def _show_watts(sid):
	
	strMsg,strDisp,strIdName=create_string_buffer(30),create_string_buffer(30),create_string_buffer(30)
	min,max=0,0	
	udwLoCritical, udwHiCritical = c_uint32(),c_uint32()
	spaceLen=0
	fFlagValue = 0
	global dwSensorType , CONFIG_NAME

	memset(strMsg,0,30)
	if  lib.LMB_HWM_GetSensorReport(sid, strMsg) != -5  :
		lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
		lib.LMB_HWM_GetSensorName(sid, strIdName)
		min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))
		if min ==999999 :
			if dwSensorType == HWM_TYPE_IPMI:
				iRet = lib.LMB_IPMI_InfoByName(strDisp, byref(stuSensorInfo))
				if iRet == ERR_Success :
					min=stuSensorInfo.fLoCritcal
					max = stuSensorInfo.fHiCritcal
				else:
					min = max = 0
			else :
				lib.LMB_HWM_GetSensorCritical(sid , byref(udwLoCritical), byref(udwHiCritical))
				min = float(udwLoCritical.value) / float(1000)
				max = float(udwHiCritical.value) / float(1000)
		else :
			max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))
		if min == 99999 or min == 999999 :
			fFlagValue |= 0x01
		if max == 99999 or max == 999999 :
			fFlagValue |= 0x01
		spaceLen=__calc_space_string(strDisp.value)
		ftemp=float(myAtoi(strMsg.value)/float(1000))  
		RoundUp_buffer=ftemp*1000
		if fFlagValue == 0x01:
			print("{:s}{:s} = {:7.3f} W\t(min = --N/A-- W, max = {:7.3f} W)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,max),end='')
			if RoundUp_buffer > max*1000 :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x02:
			print("{:s}{:s} = {:7.3f} W\t(min = {:7.3f} W, max = --N/A-- W)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,min),end='')
			if RoundUp_buffer < min*1000 :
				print(" {:s}".format(ALARM),end='')
		elif fFlagValue == 0x03:
			print("{:s}{:s} = {:7.3f} W\t(min = --N/A-- W, max = --N/A-- W)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001),end='')
		else:
			print("{:s}{:s} = {:7.3f} W\t(min = {:7.3f} W, max = {:7.3f} W)".format(strDisp.value," "*spaceLen,RoundUp_buffer*0.001,min,max),end='')
			if ((RoundUp_buffer < min*1000) or (RoundUp_buffer > max*1000)) :
				print(" {:s}".format(ALARM),end='')
		print("")
	sys.stdout.flush()



#--------------------------------------------------------------------#
def _hwm_tst():
	iRet = 0
	global CONFIG_NAME
	global dwSensorType
	fShowIpmiOnly=0



	if os.path.isfile(CONFIG_NAME) != 1 :
		CONFIG_NAME="/etc/lanner/hwm.conf"
		if os.path.isfile(CONFIG_NAME) == 1 :
			print("\033[1;31m<Note> found {:s} file, critical value will change !!!\033[m".format(CONFIG_NAME))
	else :
		print("\033[1;31m<Note> found {:s} file, critical value will change !!!\033[m".format(CONFIG_NAME))


	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 

	lib.LMB_HWM_GetSensorType(byref(dwSensorType))
	if ( dwSensorType.value == 0 ) :
		print("\033[1;31m<Warning> Hardware Monitor Type is Unknown !!!\033[m")
		return -1
	
	if dwSensorType.value == HWM_TYPE_IPMI:
		fShowIpmiOnly = 1
		print("\033[1;34m===> Hardware Monitor Type is IPMI <===\033[m")
	elif dwSensorType.value ==  HWM_TYPE_AST1400:
		print("\033[1;34m===> Hardware Monitor Type is AST-1400 <===\033[m")
	elif dwSensorType ==  HWM_TYPE_SMBUS:
		print("\033[1;34m===> Hardware Monitor Type is SMBus <===\033[m")
	elif dwSensorType.value ==  HWM_TYPE_SIO:
		print("\033[1;34m===> Hardware Monitor Type is SuperIO <===\033[m")
	else:
		print("\033[1;31m<Warning> Hardware Monitor Type is Unknown !!!\033[m")
		return -1

	print("Sensor Name        Value          LowCritical      UpperCritical   Result")
	print("-------------------------------------------------------------------------")


	#//CPU Temperature
	sid = HWMID_TEMP_CPU1
	for  xi in range(sid,sid+2) : 
		 _show_temperature(xi)
	
	#//SYS Temperature
	sid = HWMID_TEMP_SYS1
	for  xi in range(sid,sid+2) : 
		_show_temperature(xi)

	sid = HWMID_VCORE_CPU1
	for  xi in range(sid,sid+2) :
		_show_voltage(xi)
	
	#//P12V
	sid = HWMID_VOLT_P12V
	_show_voltage(sid)
	#//P5V
	sid = HWMID_VOLT_P5V
	_show_voltage(sid)
	#//P3.3V
	sid = HWMID_VOLT_P3V3
	_show_voltage(sid)
	#//P5VSB
	sid = HWMID_VOLT_P5VSB
	_show_voltage(sid)
	#//P3.3VSB
	sid = HWMID_VOLT_P3V3SB
	_show_voltage(sid)
	#//VBAT
	sid = HWMID_VOLT_VBAT
	_show_voltage(sid)
	#//1.05V
	sid = HWIID_VOLT_P1V05
	_show_voltage(sid)
	#//VCCIO
	sid = HWMID_VOLT_PVCCIO_CPU1
	for xi in range(sid,sid+2) :
		_show_voltage(xi)


	#//VCCSA
	sid = HWMID_VOLT_PVCCSA_CPU1
	for xi in range(sid,sid+2) :
		_show_voltage(xi)
	
	#//VNN
	sid = HWMID_VOLT_PVNN
	_show_voltage(sid)
	#//DDR Vlotage
	sid = HWMID_VOLT_DDRCH1
	for xi in range(sid,sid+4) :
		_show_voltage(xi)
	
	#//extern sensors
	sid = HWMID_PSU2_TEMP2 + 1
	for xi in range(sid,HWMID_TOTAL) :
		_show_voltage(xi)
	
	sid = HWMID_RPM_Fan1A
	for xi in range(10) :
		if SUPPORT_FAN_AB:
			_show_rpm(xi*2+sid)
			_show_rpm(xi*2+1+sid)
		else:
			_show_rpm(xi*2+sid)

	#/******* IPMI PSU *****/
	for xi in range(2):
		if ( fShowIpmiOnly ) :
			print("\033[2;31m================ For PSU when BMC exist ==========================\033[m")
			fShowIpmiOnly =0
		
		#//PSU VIn
		sid = HWMID_PSU1_VOLTIN + 11 * xi
		_show_voltage(sid)
		#//PSU Vout
		sid = HWMID_PSU1_VOLTOUT + 11 * xi
		_show_voltage(sid)
		#//PSU Curren In
		sid = HWMID_PSU1_CURRENTIN + 11 * xi
		_show_current(sid)
		#//PSU Curren Out
		sid = HWMID_PSU1_CURRENTOUT + 11 * xi
		_show_current(sid)
		#//PSU Power In
		sid = HWMID_PSU1_POWERIN + 11 * xi
		_show_watts(sid)
		#//PSU Power Out
		sid = HWMID_PSU1_POWEROUT + 11 * xi
		_show_watts(sid)
		#//PSU Fan 1
		sid = HWMID_PSU1_FAN1 + 11 * xi
		_show_rpm(sid)
		#//PSU Fan 2
		sid = HWMID_PSU1_FAN2 + 11 * xi
		_show_rpm(sid)
		#//PSU Temp 1
		sid = HWMID_PSU1_TEMP1 + 11 * xi
		_show_temperature(sid)
		#//PSU Temp 2
		sid = HWMID_PSU1_TEMP2 + 11 * xi
		_show_temperature(sid)

	lib.LMB_DLL_DeInit()
	return 0

		
	
#--------------------------------------------------------------------#
if __name__ == '__main__':

	hwm_util()




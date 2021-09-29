
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

	print("Usage: {:s} -info/-sensor/-watts 1/2/3".format(argv0))
	print("       {:s} -callback".format(argv0))
	print("       {:s} -test [-c filename] (default: psu.conf)".format(argv0))

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
class PSU_INFO(Structure):
	_fields_=[("ubPsuNo",c_uint8),("strubMfrId",c_uint8*33),("strubMfrModel",c_uint8*33),("strubMfrSerial",c_uint8*33),("strubMfrRevision",c_uint8*33)]

class PSU_WATTS(Structure):
	_fields_=[("ubPsuNo",c_uint8),("ubInOut",c_uint8),("fVolts",c_float),("fAmperes",c_float),("fWatts",c_float)]

class PSU_SENSORS(Structure):
	_fields_=[("ubPsuNo",c_uint8),("fTemp_1",c_float),("fTemp_2",c_float),("uwFanRpm",c_uint16)]

class PSU_CRITICAL_TABLE(Structure):
	_fields_=[("strNAME",c_uint8*20),("dwVin_110DC",c_int32*2),("dwVin_220",c_int32*2),("dwIin_110DC",c_int32*2),("dwIin_220",c_int32*2),("dwVout",c_int32*2),("dwIout",c_int32*2),("dwPin",c_int32*2),("dwPout",c_int32*2),("dwTemp1",c_int32*2),("dwTemp2",c_int32*2),("dwFan",c_int32*2),]


class INTRUSION_TIME(Structure):
	_fields_=[("uwYear",c_uint16),("ubMonth",c_uint8),("ubDay",c_uint8),("ubHour",c_uint8),("ubMinute",c_uint8),("ubSecond",c_uint8)]

class INTRUSION_MSG(Structure):
	_fields_=[("udwOccurItem",c_uint32),("udwStatus",c_uint32),("stuTime",INTRUSION_TIME)]

c_callback=CFUNCTYPE(None,INTRUSION_MSG)

def psuCallback(stuGpiMsg) :
	count = 1
	print("PSU Item  = {:04X}, Status = {:04X}, time is {:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(stuGpiMsg.udwGpis, stuGpiMsg.udwStatus, stuGpiMsg.stuTime.uwYear, stuGpiMsg.stuTime.ubMonth, stuGpiMsg.stuTime.ubDay,stuGpiMsg.stuTime.ubHour, stuGpiMsg.stuTime.ubMinute, stuGpiMsg.stuTime.ubSecond))

p_callback=c_callback(psuCallback)



#--------------------------------------------------------------------#
def _exec_callback():

	iRet=0
	xloop = 100
	
	#//intrusion callback test
	iRet = lib.LMB_PSU_IntrCallback(p_callback, 150)
	if (  iRet == ERR_Success ) :
		print("----> hook Power Supply Event Callback OK <----")
	else 	:
		print("-----> hook Power Supply Callback failure <-------")
		return
	
	print("===> wait about 10 second time <===")
	
	while(xloop>0) :		
		time.sleep(0.1)
		xloop -= 1
		#//printf("xloop = %d\n",xloop)
	
	iRet = lib.LMB_PSU_IntrCallback(None, 150)
	if (  iRet == ERR_Success ) :
		print("----> Diabled Power Supply Callback hook <----")


#--------------------------------------------------------------------#
ERR_Success	=0

PSU_WATTS_INPUT	=0
PSU_WATTS_OUTPUT=1

CONFIG_NAME	= "psu.conf"
ALARM		="\033[1;31mALARM\033[m"

LO_CRITICAL	=0
HI_CRITICAL	=1
#--------------------------------------------------------------------#

def psu_util():

	iRet,index,xi= 0,0,1
	argc=len(sys.argv)
	bsel = 0
	stuPsuInfo = PSU_INFO()
	stuWatts = PSU_WATTS()
	stuPsuSensors = PSU_SENSORS()
	str1,str2,str3,str4="","","",""
	global CONFIG_NAME


	if os.getuid() != 0  :
		_err_print("<Warning> Please uses root user !!!") 
		return -1 
	if  argc < 2  :
		__print_usage(sys.argv[0])
		return -1
	
	while  xi < argc :

		if "-info" == sys.argv[xi] : 
			bsel = 1
			if xi == argc-1 :
				_err_print("<Warning> not input PSU number")
				return -1
			bpsu = int(sys.argv[xi+1])
			xi += 2
		elif "-sensor" == sys.argv[xi] : 
			bsel = 2
			if xi == argc-1 :
				_err_print("<Warning> not input PSU number")
				return -1
			bpsu = int(sys.argv[xi+1])
			xi += 2
		elif "-watts" == sys.argv[xi] : 
			bsel = 3
			if xi == argc-1 :
				_err_print("<Warning> not input PSU number")
				return -1
			bpsu = int(sys.argv[xi+1])
			xi += 2
		elif "-callback" == sys.argv[xi] :
			bsel = 4
			xi += 1
		elif "-test" == sys.argv[xi] :
			bsel = 6
			xi += 1
		elif "-c" == sys.argv[xi] : 
			if xi == argc-1 :
				_err_print("<Warning> not input file name")
				return -1
			if  xi < argc  :
				CONFIG_NAME=sys.argv[xi+1]
			xi += 2
		else:
			__print_usage(sys.argv[0])
			return -1
			
	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 
	if bsel == 1 :
		stuPsuInfo.ubPsuNo = bpsu
		iRet = lib.LMB_PSU_DeviceInfo(byref(stuPsuInfo))
		if ( iRet == ERR_Success ) :
			for i in range(33):
				if stuPsuInfo.strubMfrId[i] != 0:			
					str1 +=(chr(stuPsuInfo.strubMfrId[i]))
				if stuPsuInfo.strubMfrModel[i] != 0:
					str2+=(chr(stuPsuInfo.strubMfrModel[i]))
				if stuPsuInfo.strubMfrSerial[i] != 0:
					str3+=(chr(stuPsuInfo.strubMfrSerial[i]))
				if stuPsuInfo.strubMfrRevision[i] != 0:
					str4+=(chr(stuPsuInfo.strubMfrRevision[i]))
			print("   PSU-{:d} MFR_ID       = {:s}".format(stuPsuInfo.ubPsuNo,str1))
			print("         MFR_MODEL    = {:s}".format(str2))
			print("         MFR_SERIAL   = {:s}".format(str3))	
			print("         MFR_REVISION = {:s}".format(str4))
		
		else 	:
			_print_error_message("LMB_PSU_DeviceInfo", iRet)	
	elif bsel == 2 :
		stuPsuSensors.ubPsuNo = bpsu
		iRet = lib.LMB_PSU_SensorInfo(byref(stuPsuSensors))
		if ( iRet == ERR_Success ) :
			print("   PSU SensorInfo : PsuNo={:d}, Temp-1={:4.1f}, Temp-2={:4.1f}, FanSpeed={:d}".format(stuPsuSensors.ubPsuNo,stuPsuSensors.fTemp_1, stuPsuSensors.fTemp_2, stuPsuSensors.uwFanRpm))
		
		else 	:
			_print_error_message("LMB_PSU_SensorInfo", iRet)
	elif bsel == 3 : #//watts
		stuWatts.ubPsuNo = bpsu	
		stuWatts.ubInOut = PSU_WATTS_INPUT
		iRet = lib.LMB_PSU_WattsInfo(byref(stuWatts))
		if  iRet == ERR_Success  :
			print("   PSU Watts  (Input): PsuNo={:d}, Volts={:4.3f}V, Amperes={:4.3f}A, Watts={:4.3f}W".format(stuWatts.ubPsuNo, stuWatts.fVolts, stuWatts.fAmperes, stuWatts.fWatts))
		else 	:
			_print_error_message("LMB_PSU_WattsInfo", iRet)

		stuWatts.ubInOut = PSU_WATTS_OUTPUT
		iRet = lib.LMB_PSU_WattsInfo(byref(stuWatts))
		if ( iRet == ERR_Success ) :
			print("   PSU Watts (Output): PsuNo={:d}, Volts={:4.3f}V, Amperes={:4.3f}A, Watts={:4.3f}W".format(stuWatts.ubPsuNo, stuWatts.fVolts, stuWatts.fAmperes, stuWatts.fWatts))
		else 	:
			_print_error_message("LMB_PSU_WattsInfo", iRet)
	elif bsel == 4 :
		_exec_callback()
	elif bsel == 5 :
		iRet = lib.LMB_PSU_QueryDevices(byref(uwData))
		if ( iRet == ERR_Success ) :
			print("   PSU QueryDevices : 0x{:02X}".format(uwData))
		
		else 	:
			_print_error_message("LMB_PSU_QueryDevices", iRet)
	elif bsel == 6 :
		_psu_tst()
	else :
		__print_usage(sys.argv[0])
		return -1




	lib.LMB_DLL_DeInit()
	return iRet
#--------------------------------------------------------------------#
def  __calc_space_string(pbStr):

	spaceLen=0
	spaceLen = 16-len(pbStr)
	return spaceLen


#--------------------------------------------------------------------#
def _psu_tst():
	iRet = 0
	global CONFIG_NAME
	uwSlotsDev,uwData=c_uint16(),c_uint16()
	fShowIpmiOnly=0
	xpsuS=0
	stuPsuInfo=PSU_INFO()
	stuWatts = PSU_WATTS()
	stuPsuSensors = PSU_SENSORS()
	stuPsuCritical = PSU_CRITICAL_TABLE()
	str1,str2,str3,str4="","","",""
	spaceLen=0
	strDisp,strIdName=create_string_buffer(30),create_string_buffer(30)

	if os.path.isfile(CONFIG_NAME) != 1 :
		CONFIG_NAME="/etc/lanner/psu.conf"
		if os.path.isfile(CONFIG_NAME) == 1 :
			print("\033[1;31m<Note> found {:s} file, critical value will change !!!\033[m".format(CONFIG_NAME))
	else :
		print("\033[1;31m<Note> found {:s} file, critical value will change !!!\033[m".format(CONFIG_NAME))


	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 

	iRet = lib.LMB_PSU_QueryDevices(byref(uwSlotsDev))
	PSU_support_number =0
	for xi in range(2) :
		if ( (uwSlotsDev.value & (0x01<<xi)) != 0 ) :
			PSU_support_number+=1
	
	print("Found PSU devices = {:d}".format(PSU_support_number))
	if ( PSU_support_number == 1 ) :
		if ( (uwSlotsDev.value & 0x03)== 0x02 ) : 
			xpsuS=1
	for no in range(xpsuS,2) :
		print("-------------Power Supply {:d}--------------".format(no+1))
		if((uwSlotsDev.value>>no) & 0x01) :
			psu_no = (no+1)
			stuPsuInfo.ubPsuNo = psu_no
			iRet = lib.LMB_PSU_DeviceInfo(byref(stuPsuInfo))
			if ( iRet == ERR_Success ) :
				for i in range(33):
					if stuPsuInfo.strubMfrId[i] != 0:			
						str1 +=(chr(stuPsuInfo.strubMfrId[i]))
					if stuPsuInfo.strubMfrModel[i] != 0:
						str2+=(chr(stuPsuInfo.strubMfrModel[i]))
					if stuPsuInfo.strubMfrSerial[i] != 0:
						str3+=(chr(stuPsuInfo.strubMfrSerial[i]))
					if stuPsuInfo.strubMfrRevision[i] != 0:
						str4+=(chr(stuPsuInfo.strubMfrRevision[i]))
				print("PSU{:d} MFR_ID       = {:s}".format(stuPsuInfo.ubPsuNo ,str1))
				print("     MFR_MODEL    = {:s}".format(str2))
				print("     MFR_SERIAL   = {:s}".format(str3))	
				print("     MFR_REVISION = {:s}".format(str4))

			else 	:
				_print_error_message("LMB_PSU_DeviceInfo", iRet)
			print("Sensor Name        Value          LowCritical      UpperCritical     Result")
			print("---------------------------------------------------------------------------")
			fpsu_table = 0
			iRet =  lib.LMB_PSU_GetCritical(stuPsuInfo.strubMfrModel,byref(stuPsuCritical))
			if ( iRet == ERR_Success ) :
				fpsu_table =1
			stuWatts.ubPsuNo = psu_no
			stuWatts.ubInOut = PSU_WATTS_INPUT
			iRet = lib.LMB_PSU_WattsInfo(byref(stuWatts))
			if iRet == ERR_Success:
				#//PSU volt
				if psu_no == 1:
					sid = HWMID_PSU1_VOLTIN
				else :
					sid = HWMID_PSU2_VOLTIN
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :
					if ( stuWatts.fVolts < float(140) ) :
						min = float(stuPsuCritical.dwVin_110DC[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwVin_110DC[HI_CRITICAL]) / float(1000)	
					
					else :
						min = float(stuPsuCritical.dwVin_220[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwVin_220[HI_CRITICAL]) / float(1000)	
					
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				RoundUp_buffer=int(stuWatts.fVolts*1000)
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8.3f} V\t(min =  --N/A-- V, max = {:8.3f} V) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),max),end='')
					if RoundUp_buffer>int(max*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8.3f} V\t(min =  {:8.3f} V, max = --N/A-- V) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),min),end='')
					if RoundUp_buffer<int(min*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8.3f} V\t(min =  --N/A-- V, max = --N/A-- V) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001)),end='')
				else :
					print("{:s}{:s}= {:8.3f} V\t(min =  {:8.3f} V, max = {:8.3f} V) ".format(strDisp.value, " "*spaceLen,float(RoundUp_buffer*0.001),min,max),end='')
					if RoundUp_buffer>int(max*1000) or RoundUp_buffer<int(min*1000):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()

				#//PSU amperes
				if psu_no == 1:
					sid = HWMID_PSU1_CURRENTIN
				else :
					sid = HWMID_PSU2_CURRENTIN
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :
					if ( stuWatts.fVolts < float(140) ) :
						min = float(stuPsuCritical.dwIin_110DC[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwIin_110DC[HI_CRITICAL]) / float(1000)	
					
					else :
						min = float(stuPsuCritical.dwIin_220[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwIin_220[HI_CRITICAL]) / float(1000)	
					
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				RoundUp_buffer=int(stuWatts.fAmperes*1000)
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8.3f} A\t(min =  --N/A-- A, max = {:8.3f} A) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),max),end='')
					if RoundUp_buffer>int(max*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8.3f} A\t(min =  {:8.3f} A, max = --N/A-- A) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),min),end='')
					if RoundUp_buffer<int(min*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8.3f} A\t(min =  --N/A-- A, max = --N/A-- A) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001)),end='')
				else :
					print("{:s}{:s}= {:8.3f} A\t(min =  {:8.3f} A, max = {:8.3f} A) ".format(strDisp.value, " "*spaceLen,float(RoundUp_buffer*0.001),min,max),end='')
					if RoundUp_buffer>int(max*1000) or RoundUp_buffer<int(min*1000):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()

				#//PSU watts
				if psu_no == 1:
					sid = HWMID_PSU1_POWERIN
				else :
					sid = HWMID_PSU2_POWERIN
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :

						min = float(stuPsuCritical.dwPin[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwPin[HI_CRITICAL]) / float(1000)				
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				RoundUp_buffer=int(stuWatts.fWatts*1000)
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8.3f} W\t(min =  --N/A-- W, max = {:8.3f} W) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),max),end='')
					if RoundUp_buffer>int(max*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8.3f} W\t(min =  {:8.3f} W, max = --N/A-- W) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),min),end='')
					if RoundUp_buffer<int(min*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8.3f} W\t(min =  --N/A-- W, max = --N/A-- W) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001)),end='')
				else :
					print("{:s}{:s}= {:8.3f} W\t(min =  {:8.3f} W, max = {:8.3f} W) ".format(strDisp.value, " "*spaceLen,float(RoundUp_buffer*0.001),min,max),end='')
					if RoundUp_buffer>int(max*1000) or RoundUp_buffer<int(min*1000):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()
			else 	:
				_print_error_message("LMB_PSU_WattsInfo", iRet)

			stuWatts.ubInOut = PSU_WATTS_OUTPUT
			iRet = lib.LMB_PSU_WattsInfo(byref(stuWatts))
			if iRet == ERR_Success:
				#//PSU volt
				if psu_no == 1:
					sid = HWMID_PSU1_VOLTOUT
				else :
					sid = HWMID_PSU2_VOLTOUT
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :

						min = float(stuPsuCritical.dwVout[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwVout[HI_CRITICAL]) / float(1000)				
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				RoundUp_buffer=int(stuWatts.fVolts*1000)
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8.3f} V\t(min =  --N/A-- V, max = {:8.3f} V) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),max),end='')
					if RoundUp_buffer>int(max*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8.3f} V\t(min =  {:8.3f} V, max = --N/A-- V) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),min),end='')
					if RoundUp_buffer<int(min*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8.3f} V\t(min =  --N/A-- V, max = --N/A-- V) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001)),end='')
				else :
					print("{:s}{:s}= {:8.3f} V\t(min =  {:8.3f} V, max = {:8.3f} V) ".format(strDisp.value, " "*spaceLen,float(RoundUp_buffer*0.001),min,max),end='')
					if RoundUp_buffer>int(max*1000) or RoundUp_buffer<int(min*1000):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()

				#//PSU amperes
				if psu_no == 1:
					sid = HWMID_PSU1_CURRENTOUT
				else :
					sid = HWMID_PSU2_CURRENTOUT
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :

						min = float(stuPsuCritical.dwIout[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwIout[HI_CRITICAL]) / float(1000)				
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				RoundUp_buffer=int(stuWatts.fAmperes*1000)
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8.3f} A\t(min =  --N/A-- A, max = {:8.3f} A) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),max),end='')
					if RoundUp_buffer>int(max*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8.3f} A\t(min =  {:8.3f} A, max = --N/A-- A) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),min),end='')
					if RoundUp_buffer<int(min*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8.3f} A\t(min =  --N/A-- A, max = --N/A-- A) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001)),end='')
				else :
					print("{:s}{:s}= {:8.3f} A\t(min =  {:8.3f} A, max = {:8.3f} A) ".format(strDisp.value, " "*spaceLen,float(RoundUp_buffer*0.001),min,max),end='')
					if RoundUp_buffer>int(max*1000) or RoundUp_buffer<int(min*1000):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()


				#//PSU watts
				if psu_no == 1:
					sid = HWMID_PSU1_POWEROUT
				else :
					sid = HWMID_PSU2_POWEROUT
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :

						min = float(stuPsuCritical.dwPout[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwPout[HI_CRITICAL]) / float(1000)				
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				RoundUp_buffer=int(stuWatts.fWatts*1000)
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8.3f} W\t(min =  --N/A-- W, max = {:8.3f} W) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),max),end='')
					if RoundUp_buffer>int(max*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8.3f} W\t(min =  {:8.3f} W, max = --N/A-- W) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001),min),end='')
					if RoundUp_buffer<int(min*1000) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8.3f} W\t(min =  --N/A-- W, max = --N/A-- W) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.001)),end='')
				else :
					print("{:s}{:s}= {:8.3f} W\t(min =  {:8.3f} W, max = {:8.3f} W) ".format(strDisp.value, " "*spaceLen,float(RoundUp_buffer*0.001),min,max),end='')
					if RoundUp_buffer>int(max*1000) or RoundUp_buffer<int(min*1000):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()
			else 	:
				_print_error_message("LMB_PSU_WattsInfo", iRet)

			stuPsuSensors.ubPsuNo = psu_no
			iRet = lib.LMB_PSU_SensorInfo(byref(stuPsuSensors))
			if iRet == ERR_Success:
				#//PSU temp 1
				if psu_no == 1:
					sid = HWMID_PSU1_TEMP1
				else :
					sid = HWMID_PSU2_TEMP1
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :

						min = float(stuPsuCritical.dwTemp1[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwTemp1[HI_CRITICAL]) / float(1000)				
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				RoundUp_buffer=int(stuPsuSensors.fTemp_1*10)
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8.1f} C\t(min =  --N/A-- C, max = {:8.1f} C) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.1),max),end='')
					if RoundUp_buffer>int(max*10) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8.1f} C\t(min =  {:8.1f} C, max = --N/A-- C) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.1),min),end='')
					if RoundUp_buffer<int(min*10) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8.1f} C\t(min =  --N/A-- C, max = --N/A-- C) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.1)),end='')
				else :
					print("{:s}{:s}= {:8.1f} C\t(min =  {:8.3f} C, max = {:8.1f} C) ".format(strDisp.value, " "*spaceLen,float(RoundUp_buffer*0.1),min,max),end='')
					if RoundUp_buffer>int(max*10) or RoundUp_buffer<int(min*10):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()
				#//PSU temp 2
				if psu_no == 1:
					sid = HWMID_PSU1_TEMP1
				else :
					sid = HWMID_PSU2_TEMP1
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :

						min = float(stuPsuCritical.dwTemp2[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwTemp2[HI_CRITICAL]) / float(1000)				
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				RoundUp_buffer=int(stuPsuSensors.fTemp_2*10)
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8.1f} C\t(min =  --N/A-- C, max = {:8.1f} C) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.1),max),end='')
					if RoundUp_buffer>int(max*10) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8.1f} C\t(min =  {:8.1f} C, max = --N/A-- C) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.1),min),end='')
					if RoundUp_buffer<int(min*10) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8.1f} C\t(min =  --N/A-- C, max = --N/A-- C) ".format(strDisp.value, ' '*spaceLen,float(RoundUp_buffer*0.1)),end='')
				else :
					print("{:s}{:s}= {:8.1f} C\t(min =  {:8.1f} C, max = {:8.1f} C) ".format(strDisp.value, " "*spaceLen,float(RoundUp_buffer*0.1),min,max),end='')
					if RoundUp_buffer>int(max*10) or RoundUp_buffer<int(min*10):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()
				#//PSU Fan speed
				if psu_no == 1:
					sid = HWMID_PSU1_FAN1
				else :
					sid = HWMID_PSU2_FAN1
				lib.LMB_HWM_GetSensorDisplay(sid, strDisp)
				spaceLen=__calc_space_string(strDisp.value)
				lib.LMB_HWM_GetSensorName(sid, strIdName)
				min = binaryToFloat(lib2.read_profile_int(strIdName.value, "min", 0, CONFIG_NAME))		
				if ( min == 999999 and fpsu_table==1 )  :

						min = float(stuPsuCritical.dwFan[LO_CRITICAL]) / float(1000)
						max = float(stuPsuCritical.dwFan[HI_CRITICAL]) / float(1000)				
					
				else  :
					max = binaryToFloat(lib2.read_profile_int(strIdName.value, "max", 0, CONFIG_NAME))

				fFlagValue=0
				if min == 99999 or min == 999999 :
					fFlagValue |= 0x01
				if max == 99999 or max == 999999 :
					fFlagValue |= 0x02
				if fFlagValue == 0x01 :
					print("{:s}{:s}= {:8d} rpm\t(min =  --N/A-- rpm, max = {:6d} rpm) ".format(strDisp.value, ' '*spaceLen,stuPsuSensors.uwFanRpm,int(max)),end='')
					if stuPsuSensors.uwFanRpm>int(max) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x02 :
					print("{:s}{:s}= {:8d} rpm\t(min =  {:6d} rpm, max = --N/A-- rpm) ".format(strDisp.value, ' '*spaceLen,stuPsuSensors.uwFanRpm,int(min)),end='')
					if stuPsuSensors.uwFanRpm<int(min) :
						print("{:s}".format(ALARM),end='')
				elif fFlagValue == 0x03 :
					print("{:s}{:s}= {:8d} rpm\t(min =  --N/A-- rpm, max = --N/A-- rpm) ".format(strDisp.value, ' '*spaceLen,stuPsuSensors.uwFanRpm),end='')
				else :
					print("{:s}{:s}= {:8d} rpm\t(min =  {:6d} rpm, max = {:6d} rpm) ".format(strDisp.value, ' '*spaceLen,stuPsuSensors.uwFanRpm,int(min),int(max)),end='')
					if stuPsuSensors.uwFanRpm>int(max) or stuPsuSensors.uwFanRpm<int(min):
						print("{:s}".format(ALARM),end='')
				print("")
				sys.stdout.flush()
			else 	:
				_print_error_message("LMB_PSU_Status", iRet)
			iRet = lib.LMB_PSU_Status(psu_no, byref(uwData))
			if ( iRet == ERR_Success ) :
				print("Current PSU-{:d} devices status:0x{:04X}".format(psu_no, uwData.value))
			else	:
				_print_error_message("LMB_PSU_Status", iRet)
		else :
			print("Power supply {:d} no exist [ALARM]".format(no+1))
	sys.stdout.flush()
	lib.LMB_DLL_DeInit()
	return 0
	
#--------------------------------------------------------------------#
def binaryToFloat(value):
	value=bin(value)[2:]
	hx = int(value,2)
	return struct.unpack("f",struct.pack("I",hx))[0]

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
if __name__ == '__main__':
	psu_util()


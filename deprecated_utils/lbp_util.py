
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

	print("Usage: {:s} [-s0/../-s8] [-info/-status/-save/-factory]".format(argv0))
	print("       {:s} [-s0/../-s8] [-sysoff/-juston/-runtime]  #hex".format(argv0))
	print("       {:s} [-s0/../-s8] [-p1/../-p4] [-enable/-disable]".format(argv0))
	print("       {:s} [-s0/../-s8] [-t1/-t2] -second #dec -effect #hex".format(argv0))
	print("       {:s} [-s0/../-s8] [-t1/-t2] [-start/-reload/-stop]".format(argv0))
	print("       {:s} [-query] ".format(argv0))
	print("	paramerer:")
	print("	-s0/../-s8 	: assign slot device number, -s0 is onboard device(default)")
	print("	-p1/../-p4 	: assign pair number (runtime stage)")
	print("	-t1/-t2 	: assign time-1 or timer-2")
	print("	-enable/-disable: enable or disable runtime assign pair number (runtime stage)")
	print("	-info		: getting information")
	print("	-status		: getting bypass status")
	print("	-save		: save current config to default")
	print("	-factory	: loading factory config value (not save)")
	print("	-sysoff #hex	: system-off pairs setting")
	print("	-juston	#hex	: just-on pairs setting")
	print("	-runtime #hex	: runtime pairs setting")
	print("	-second #dec	: counter setting for bypass timer (1~255)")
	print("	-effect #hex	: setting after times-out which pair bypass enable")
	print("	-start/-reload/-stop	: start, reload and stop timer")

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
TYPE_INFO	=1
TYPE_STATUS	=2
TYPE_PAIR	=3
TYPE_SYSOFF	=4
TYPE_JUSTON	=5
TYPE_RUNTIME	=6
TYPE_TIMER	=7
TYPE_SAVE	=8
TYPE_FACTORY	=9
TYPE_QUERY	=10

PAIR_DISABLE	=1
PAIR_ENABLE	=2

TIMER_START	=1
TIMER_STOP	=2
TIMER_RELOAD	=3

LAN_TYPE_UNKNOW	=0
LAN_TYPE_COPPER	=1
LAN_TYPE_FIBEr	=2

PAIR_BYPASS_NOASSIGN	=0
PAIR_BYPASS_ENABLE	=1
PAIR_BYPASS_DISCONNECT	=2

ERR_Success	=0

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
class LBPDEV_INFO(Structure):
	_fields_=[("ubSlotIndex",c_uint8),("ubType",c_uint8),("ubVersion",c_uint8*2),("ubModules",c_uint8),("ubSystemOff_Pairs",c_uint8),("ubJustOn_Pairs",c_uint8),("ubRuntime_Pairs",c_uint8),("uwTimer1_MaxSec",c_uint16),("uwTimer2_MaxSec",c_uint16),("uwTimer3_MaxSec",c_uint16)]

class PAIRS_STATUS(Structure):
	_fields_=[("ubSlotIndex",c_uint8),("ubSystemOff_PairsBypass",c_uint8),("ubJustOn_PairsBypass",c_uint8),("ubRuntime_PairsBypass",c_uint8),("ubJustOn_PortsDisconnect",c_uint8),("ubRuntime_PortsDisconnect",c_uint8)]

class LBP_TIMERCFG(Structure):
	_fields_=[("ubTimerNo",c_uint8),("uwTimeSec",c_uint16),("ubAction",c_uint8),("ubEffect",c_uint8)]
#--------------------------------------------------------------------#
def lbp_util():


	iRet,index,xi= 0,0,1
	argc=len(sys.argv)
	bType , bSubType =0,0
	bEnable,wAddr,bTimer=0,0,0
	bSlot=-1
	bEffect=0xFF
	dwCount,dwData, dwEffect =-1,-1,-1
	LbpDevInfo=LBPDEV_INFO()
	PairsStatus=PAIRS_STATUS()
	stuTimerCfg =LBP_TIMERCFG()
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
		elif 	"-t1" == sys.argv[xi] :
			bType = TYPE_TIMER
			bTimer =1 
			xi += 1
		elif 	"-t2" == sys.argv[xi] :
			bType = TYPE_TIMER
			bTimer =2 
			xi += 1
		elif 	"-p1" == sys.argv[xi] :
			bType = TYPE_PAIR
			bPair = 1
			xi += 1
		elif 	"-p2" == sys.argv[xi] :
			bType = TYPE_PAIR
			bPair = 2
			xi += 1
		elif 	"-p3" == sys.argv[xi] :
			bType = TYPE_PAIR
			bPair = 3
			xi += 1
		elif 	"-p4" == sys.argv[xi] :
			bType = TYPE_PAIR
			bPair = 4
			xi += 1
		elif 	"-info" == sys.argv[xi] :
			bType=TYPE_INFO
			xi +=1
		elif 	"-status" == sys.argv[xi] :
			bType=TYPE_STATUS
			xi +=1
		elif 	"-save" == sys.argv[xi] :
			bType=TYPE_SAVE
			xi +=1
		elif 	"-factory" == sys.argv[xi] :
			bType=TYPE_FACTORY
			xi +=1
		elif 	"-query" == sys.argv[xi] :
			bType=TYPE_QUERY
			xi +=1
		elif 	"-enable" == sys.argv[xi] :
			bEnable = PAIR_ENABLE
			xi +=1
		elif 	"-disable" == sys.argv[xi] :
			bEnable = PAIR_DISABLE
			xi +=1
		elif 	"-start" == sys.argv[xi] :
			bSubType = TIMER_START
			xi +=1
		elif 	"-stop" == sys.argv[xi] :
			bSubType = TIMER_STOP
			xi +=1
		elif 	"-reload" == sys.argv[xi] :
			bSubType = TIMER_RELOAD
			xi +=1
		elif 	"-runtime" == sys.argv[xi] :
			bType = TYPE_RUNTIME
			if xi != argc-1:
				dwData = int(sys.argv[xi+1],base=16)
				print("Set Runtime Pairs is 0x{:02X}".format(dwData))
			xi +=2
		elif 	"-sysoff" == sys.argv[xi] :
			bType = TYPE_SYSOFF
			if xi != argc-1:
				dwData = int(sys.argv[xi+1],base=16)
				print("Set SystemOff Pairs is 0x{:02X}".format(dwData))
			xi +=2
		elif 	"-juston" == sys.argv[xi] :
			bType = TYPE_JUSTON
			if xi != argc-1:
				dwData = int(sys.argv[xi+1],base=16)
				print("Set JustOn Pairs is 0x{:02X}".format(dwData))
			xi +=2
		elif 	"-effect" == sys.argv[xi] :
			if xi != argc-1:
				dwEffect = int(sys.argv[xi+1],base=16)
				print("Set Effect Pairs is 0x{:02X}".format(dwEffect))
			xi +=2
		elif 	"-second" == sys.argv[xi] :
			if xi != argc-1:
				dwCount = int(sys.argv[xi+1])
				print("Set Effect Pairs is 0x{:02X}".format(dwCount))
			xi +=2
		else:
			__print_usage(sys.argv[0])
			return -1

	if ( (bSlot == -1 or bSlot >= 9) and bType != TYPE_QUERY) :
		__print_usage(argv[0])
		return -1

	iRet = lib.LMB_DLL_Init()
	if  iRet != ERR_Success :
		_print_error_message("LMB_DLL_Init", iRet) 
		_err_print("please confirm the API libraries is matched this platform") 
		return -1 


	elif bType == TYPE_INFO:
		print("===========> Bypass Device Information : Slot-{:d}".format(bSlot))
		iRet = lib.LMB_LBP_DeviceInfo(bSlot, byref(LbpDevInfo))
		if iRet == ERR_Success:
			if LbpDevInfo.ubType == LAN_TYPE_COPPER:
				print("Controller Type is Copper")
			elif LbpDevInfo.ubType == LAN_TYPE_FIBER:
				print("Controller Type is Fiber")
			else :
				print("Controller Type is unknown")
			print("	Version: {:d}.{:d}".format(LbpDevInfo.ubVersion[0], LbpDevInfo.ubVersion[1]))
			print("	Modules: 0x{:02X}".format(LbpDevInfo.ubModules))
			print("	SystemOff Pairs: 0x{:02X}".format(LbpDevInfo.ubSystemOff_Pairs))
			print("	JustOn Pairs: 0x{:02X}".format(LbpDevInfo.ubJustOn_Pairs))
			print("	Runtime Pairs: 0x{:02X}".format(LbpDevInfo.ubRuntime_Pairs))
			print("	Timer1 MaxSec: {:d} seconds".format(LbpDevInfo.uwTimer1_MaxSec))
			print("	Timer2 MaxSec: {:d} seconds".format(LbpDevInfo.uwTimer2_MaxSec))
			print("	Timer3 MaxSec: {:d} seconds".format(LbpDevInfo.uwTimer3_MaxSec))
		else :
			_print_error_message("LMB_LBP_DeviceInfo", iRet)
	elif bType == TYPE_STATUS:
		print("===========> GetPairsStatus: Slot-{:d}".format(bSlot))
		iRet =  lib.LMB_LBP_GetPairsStatus(bSlot, byref(PairsStatus))
		if iRet == ERR_Success:
			print("	SystemOff_PairsBypass: 0x{:02X}".format(PairsStatus.ubSystemOff_PairsBypass))
			print("	JustOn_PairsBypass: 0x{:02X}".format(PairsStatus.ubJustOn_PairsBypass))
			print("	Runtime_PairsBypass: 0x{:02X}".format(PairsStatus.ubRuntime_PairsBypass))
			print("	JustOn_PortsDisconnect: 0x{:02X}".format(PairsStatus.ubJustOn_PortsDisconnect))
			print("	ubRuntime_PortsDisconnect: 0x{:02X}".format(PairsStatus.ubRuntime_PortsDisconnect))
		else:
			_print_error_message("LMB_LBP_GetPairsStatus", iRet)

	elif bType == TYPE_RUNTIME :
		print("===========> Set Runtime Pairs: Slot-{:d}, Pairs 0x{:02X}".format(bSlot,(dwData & 0xff)))
		if dwData == -1 :
			print("<Error> No value input !!!")
		else:
			iRet = lib.LMB_LBP_SetAllPairs(bSlot,(dwData & 0xff))
			if iRet == ERR_Success :
				print("==> LMB_LBP_SetAllPairs OK")
			else:
				_print_error_message("LMB_LBP_SetAllPairs", iRet)
	elif bType == TYPE_SYSOFF:
		print("===========> Set SystemOff Pairs: Slot-{:d}, Pairs 0x{:02X}".format(bSlot,(dwData & 0xff)))
		if dwData == -1 :
			print("<Error> No value input !!!")
		else:
			iRet =  lib.LMB_LBP_SetSystemOffPairs(bSlot,(dwData & 0xff))
			if iRet == ERR_Success :
				print("==> LMB_LBP_SetAllPairs OK")
			else:
				_print_error_message("LMB_LBP_SetSystemOffPairs", iRet)
	elif bType == TYPE_JUSTON :
		print("===========> Set Just-On Pairs: Slot-{:d}, Pairs 0x{:02X}".format(bSlot,(dwData & 0xff)))
		if dwData == -1 :
			print("<Error> No value input !!!")
		else:
			iRet =  lib.LMB_LBP_SetJustOnPairs(bSlot,(dwData & 0xff))
			if iRet == ERR_Success :
				print("==> LMB_LBP_SetJustOnPairs OK")
			else:
				_print_error_message("LMB_LBP_SetJustOnPairs", iRet)
	elif bType == TYPE_PAIR :
		print("===========> Set Runtime Pairs: Slot-{:d}, Pair-{:d}".format(bSlot, bPair))
		if  bPair == 0 :
			print("<Error> No pair setting !!!")  
		if  bEnable == 0 : 
			print("<Error> No -enable or -disable setting !!!")
		iRet =  lib.LMB_LBP_SetPairBypass(bSlot, bPair, bEnable-1)
	elif bType == TYPE_TIMER :
		if bSubType == TIMER_START :
			print("===========> starting Slot-{:d}, Timer-{:d}".format(bSlot, bTimer))
			iRet= lib.LMB_LBP_TimerStart(bSlot, bTimer)
			if iRet == ERR_Success :
				print("LMB_LBP_TimerStart OK")
			else:
				_print_error_message("LMB_LBP_TimerStart", iRet)
		elif bSubType == TIMER_STOP :
			print("===========> stop Slot-{:d}, Timer-{:d}".format(bSlot, bTimer))
			iRet= lib.LMB_LBP_TimerStop(bSlot, bTimer)
			if iRet == ERR_Success :
				print("LMB_LBP_TimerStop OK")
			else:
				_print_error_message("LMB_LBP_TimerStop", iRet)
		elif bSubType == TIMER_RELOAD :
			print("===========> reload Slot-{:d}, Timer-{:d}".format(bSlot, bTimer))
			iRet= lib.LMB_LBP_TimerTick(bSlot, bTimer)
			if iRet == ERR_Success :
				print("LMB_LBP_TimerTick OK")
			else:
				_print_error_message("LMB_LBP_TimerTick", iRet)
		else:
			print("===========> Set Slot-{:d}, Timer-{:d}, {:d} second, pairs 0x{:02X}".format(bSlot, bTimer, dwCount, (dwEffect&0xFF)))
			if  dwCount == -1 :
				print("<Error> No timer count setting !!!") 
				return
			if  dwEffect == -1  :
				print("<Error> No effect pairs setting !!!")
				return
			stuTimerCfg.ubTimerNo = bTimer
			stuTimerCfg.uwTimeSec = (dwCount & 0xFFFF)
			stuTimerCfg.ubAction = PAIR_BYPASS_ENABLE
			stuTimerCfg.ubEffect = (dwEffect & 0xFF)
			iRet =  lib.LMB_LBP_TimerConfig(bSlot, stuTimerCfg)
			if iRet == ERR_Success :
				print("LMB_LBP_TimerConfig OK")
			else:
				_print_error_message("LMB_LBP_TimerConfig", iRet)
	elif bType == TYPE_SAVE :
		iRet =  lib.LMB_LBP_SaveConfig(bSlot)
		if iRet == ERR_Success :
			print("LMB_LBP_SaveConfig OK")
		else:
			_print_error_message("LMB_LBP_SaveConfig", iRet)
	elif bType == TYPE_FACTORY :
		iRet =  lib.LMB_LBP_FactoryReset(bSlot)
		if iRet == ERR_Success :
			print("LMB_LBP_FactoryReset OK")
		else:
			_print_error_message("LMB_LBP_FactoryReset", iRet)
	elif bType == TYPE_QUERY :
		_lbp_query()
	else:
		__print_usage(sys.argv[0])
		return -1

	lib.LMB_DLL_DeInit()
	return iRet


def _lbp_query():
	iRet=0
	uwSlotsDev=c_uint16(0)
	iRet = lib.LMB_LBP_QueryDevices(byref(uwSlotsDev))
	if ( iRet == ERR_Success ) :
		print("EEPROM devises exist 0x{:04X}".format(uwSlotsDev.value))
	else			   :
		_print_error_message("LMB_LBP_QueryDevices", iRet)
if __name__ == '__main__':
	lbp_util()



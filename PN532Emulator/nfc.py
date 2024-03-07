import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
import time

# IMPORRT COMMANDS FOR PCD

from adafruit_pn532.adafruit_pn532 import _COMMAND_INDATAEXCHANGE
from adafruit_pn532.adafruit_pn532 import _COMMAND_INLISTPASSIVETARGET
from adafruit_pn532.adafruit_pn532 import _COMMAND_INPSL

#IMPORT COMMANDS FOR PICC

from adafruit_pn532.adafruit_pn532 import _COMMAND_TGINITASTARGET
from adafruit_pn532.adafruit_pn532 import _COMMAND_TGRESPONSETOINITIATOR
from adafruit_pn532.adafruit_pn532 import _COMMAND_TGGETDATA
from adafruit_pn532.adafruit_pn532 import _COMMAND_TGSETDATA
# singleton class to set up SPI port to communicate with adafruit board
class NFC_setup():
	count=0
	spi=None
	cip=None
	cs_pin=None
	def __init__(self):
		raise Exception("please use initializare for avoiding multiple NFC objects")


	@classmethod	
	def initializare(cls):
		if (cls.count==0):
			cls.spi=busio.SPI(board.SCK,board.MOSI,board.MISO)
			cls.cs_pin=DigitalInOut(board.D5)
			cls.cip=PN532_SPI(cls.spi,cls.cs_pin,debug=False)
			cls.count+=1
			return cls.cip
		else:
			return cls.cip


#board manager - created for lor lvl interaction with the board
class board_mngr_PCD():
	
	#create new NFC socket,
	def __init__(self):
		print("Socket created")
		self.adafruit_pn532=NFC_setup.initializare()


	#check firmware version and the connection	
	def get_firmware_version(self):	
		return self.adafruit_pn532.firmware_version

	#mifare cards config	
	def mifare_config(self):
		self.adafruit_pn532.SAM_configuration()
		print("Socket set up to be compatible with ISO 14443 Card")

	#return bytecode - raw hex
	#function used only to get the raw UID of the card -> unable to send further commands to the card
	def get_raw_UID(self):
		UID=self.adafruit_pn532.read_passive_target(timeout=0.5)
		if (UID!=None):
			print(len(UID))
			return UID
		else :
			return("Card Not Detected") 

	#function used only to get the string version  of the card UID  -> unable to send further commands to the card
	def get_UID(self):
		UID=self.adafruit_pn532.read_passive_target(timeout=0.5)
		list_UID=[]
		if (UID!=None):
			for i in range(0,len(UID)):
				list_UID.append(UID[i])
			
			return list_UID
		else:
			return("Card Not Detected")		

	#function used to enlist a card and use it's UID for further data echange		
	def enlist_target(self):
	 		enlisted=self.adafruit_pn532.read_passive_target(timeout=2)
	 		if (enlisted):
	 			print(enlisted)
	 			return 1 
	 		else :
	 			return 0


	 #function used to config board as a virtual card 

	def config_PICC(self):
		MODE = [0x05]   # 5 is for PICC only
		NFC_SENS_RES = [0x04,0x00]
		NFC_ID=[0x01,0x02,0x03]
		SEL_RES=[0x20]
		FELICA_PARAMETERS=[0x01,0xFE,0x05,0x01,0x86,0x04,0x02,0x02,0x03,0x00,0x4B,0x02,0x4F,0x49,0x8A,0x00,0xFF,0xFF]
		NFCID3t=[0x01,0x01,0x66,0x6D,0x01,0x01,0x10,0x02,0x00,0x00]
		L_GENERAL_BYTES=[0x00]

		L_HISTORICAL_BYTES=[0x0]


		

		connection_response=self.adafruit_pn532.call_function(_COMMAND_TGINITASTARGET,params=MODE+NFC_SENS_RES+NFC_ID+SEL_RES+FELICA_PARAMETERS+NFCID3t+L_GENERAL_BYTES+L_HISTORICAL_BYTES,response_length=255)
		print("RATS is :"+str(connection_response));




	def PICC_GET_DATA(self):
		get_data=self.adafruit_pn532.call_function(_COMMAND_TGGETDATA,response_length=255)
		print(get_data)
		if get_data :
			return 1
		else :
			return 0
	

	def PICC_SET_DATA(self , data ) :
		set_data=self.adafruit_pn532.call_function(_COMMAND_TGSETDATA,params=data,response_length=255)


	#function used to activate ISO/DEP ISO14443-4 data exchange speed 
	# Allowed values 106 kbps / 212 kbps /424 kbps			
	def configure_PPS (self,val_sp): 			
		speed=[0x00,0x01,0x02]
		#speed[0] - >106 kbps
		#speed[1] - >212 kbps
		#speed[2] - >424 kbps
		
		if(val_sp>2 or val_sp<0):
			val_sp=0
			prin("Default speed Configuration ISO14443-4")

		val_sp_dict={0:"106kbps",1:"212kbps",2:"424kbps"}
		print("ISODEP Speed"+val_sp_dict[val_sp])
		PPS=send=self.adafruit_pn532.call_function(_COMMAND_INPSL,params=[0x01,speed[val_sp],speed[val_sp]])

	def write_apdu(self,apdu):
		send=self.adafruit_pn532.call_function(_COMMAND_INDATAEXCHANGE,params=[0x01]+apdu,response_length=255)
		if (send):
			print(send)

#program entry point 

#Set MANAGER - AVAILABLE FOR PICC AND PCD 
board_manager=board_mngr_PCD()
print(board_manager.get_firmware_version())
board_manager.mifare_config()




#loop
while(True):

	#CONFIG AS PCD
	#card_status=board_manager.enlist_target()
	
	#CONFIG AS PICC
	config_PICC=board_manager.config_PICC()		
	
	data=board_manager.PICC_GET_DATA()
	if data :
		board_manager.PICC_SET_DATA([0x90,0x00])
	data=board_manager.PICC_GET_DATA()
	if data:
		board_manager.PICC_SET_DATA([0x90,0x00])
	
	# SEND APDU
	#if(card_status):
		#CONFIG PPS
		#board_manager.configure_PPS(0)

		#WRITE APDU
		#board_manager.write_apdu([0x23,0x49])
		#board_manager.write_apdu([0x00,0xA4,0x04,0x00,0x10,0xA0,0x00,0x00,0x06,0x04,0x53,0x6D,0x61,0x72,0x74,0x4B,0x65,0x79,0x00,0x01,0x01])
	time.sleep(1)



#[0x00,0xA4,0x04,0x00,0x10,0xA0,0x00,0x00,0x06,0x04,0x53,0x6D,0x61,0x72,0x74,0x4B,0x65,0x79,0x00,0x01,0x01]

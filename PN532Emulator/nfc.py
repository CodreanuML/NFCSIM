import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
import time
import logging



# IMPORRT COMMANDS FOR ISO14443 Type A PCD"

from adafruit_pn532.adafruit_pn532 import _COMMAND_INDATAEXCHANGE
from adafruit_pn532.adafruit_pn532 import _COMMAND_INLISTPASSIVETARGET
from adafruit_pn532.adafruit_pn532 import _COMMAND_INPSL

#IMPORT COMMANDS FOR ISO14443 Type A PICC"

from adafruit_pn532.adafruit_pn532 import _COMMAND_TGINITASTARGET
from adafruit_pn532.adafruit_pn532 import _COMMAND_TGRESPONSETOINITIATOR
from adafruit_pn532.adafruit_pn532 import _COMMAND_TGGETDATA
from adafruit_pn532.adafruit_pn532 import _COMMAND_TGSETDATA


#IMPORT COMMAND FOR MIFARE CLASSIC 


from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A 
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B 


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



#board manager - created for low lvl interaction with NFC board - >>> used when board is set up as PCD (reader/Writer) - > Mifare Classic Version
class board_manager_MIFARE():
	#create new NFC PCD socket,
	def __init__(self):
		logger_main.info("Socket created - Mifare classic")		
		self.adafruit_pn532=NFC_setup.initializare()


	#check firmware version and the connection	
	def get_firmware_version(self):	
		return self.adafruit_pn532.firmware_version

	#config SAM on chipset	
	def config(self):
		self.adafruit_pn532.SAM_configuration()

	#get a passive target	
	def read_passive_target(self,timeout):
		uid=self.adafruit_pn532.read_passive_target(timeout=timeout)
		return uid

	#authenticate command	
	def mifare_classic_authenticate_block(self,uid,block_number: int,key_number:[0x60, 0x61],key) -> bool:
		status=self.adafruit_pn532.mifare_classic_authenticate_block(uid,block_number,key_number,key)
		if status:
			logger_main.info("Key block successfully logged !")
		else:
			logger_main.info("Key block login failed ! ")

	#read block		
	def mifare_classic_read_block(self, block_number: int):  	
		read_value =self.adafruit_pn532.mifare_classic_read_block(block_number)
		if read_value==None :
			logger_main.info("Block not read !")
		else : 
			return read_value

	#write block		
	def mifare_classic_write_block(self, block_number: int, data) -> bool:
		write_value = self.adafruit_pn532.mifare_classic_write_block(block_number,data)
		if write_value :
			logger_main.info("Block successfully written")
		else :
			logger_main.info("Block writing failed !")	

    #format a block to be a value block
	def mifare_classic_fmt_value_block(self, block_number: int, initial_value: int, address_block: int = 0) -> bool:
		status =self.adafruit_pn532.mifare_classic_fmt_value_block(block_number,initial_value)
		if status :
			logger_main.info("Block number {no} successfully formated to value block !" .format(no=block_number))
		else :
			logger_main.info("Block number {no} formatation to value block failed ! " .format(no=block_number))

	#return a value block value		
	def mifare_classic_get_value_block(self, block_number: int) -> int:
		get_result = self.adafruit_pn532.mifare_classic_get_value_block(block_number)
		logger_main.info("Block number " + str(block_number) + " has value " + str(get_result))

	#subtract a value from a value block		
	def mifare_classic_sub_value_block(self, block_number: int, amount: int) -> bool:
		substraciton_result=self.adafruit_pn532.mifare_classic_sub_value_block(block_number,amount)
		if substraciton_result :
			logger_main.info("Block number {no} successfully decreased with value {value} !".format(no=block_number,value=amount))
		else :
			logger_main.info("Substraction failed ! ")

	#add a value to a value block		
	def mifare_classic_add_value_block(self, block_number: int, amount: int) -> bool:
		add_result=self.adafruit_pn532.mifare_classic_add_value_block(block_number,amount)
		if add_result :
			logger_main.info("Block number {no} successfully incresed with value {value} !".format(no=block_number,value=amount))
		else:
			logger_main.info("Adition failed !")



#board manager - created for low lvl interaction with NFC board - >>> used when board is set up as PCD (reader/Writer)
class board_manager_PCD():
	
	#create new NFC PCD socket,
	def __init__(self):
		logger_main.info("Socket created - ISO14443 Type A PCD")
		
		self.adafruit_pn532=NFC_setup.initializare()


	#check firmware version and the connection	
	def get_firmware_version(self):	
		return self.adafruit_pn532.firmware_version

	#config SAM on chipset	
	def config(self):
		self.adafruit_pn532.SAM_configuration()
		

	#return bytecode - raw hex
	#function used only to get the raw UID of the card -> unable to send further commands to the card
	def get_raw_UID(self):
		UID=self.adafruit_pn532.read_passive_target(timeout=0.5)
		if (UID!=None):
			
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

	#function used to activate ISO ISO14443-3 anticolission protocol
	#function used to enlist a card and use it's UID for further data echange		
	def enlist_target(self):
		enlisted_UID=self.adafruit_pn532.read_passive_target(timeout=2)
		list_UID=[]
		uid_type=0
		uid_values={1:"single",2:"double",3:"triple"}
		if (enlisted_UID):
			logger_main.info("Card Enlisted")
			for i in range(0,len(enlisted_UID)):

				list_UID.append(enlisted_UID[i])
				uid_type=len(list_UID)//3
			try: 
				logger_main.info("UID Type -> {uidtype}".format(uidtype=uid_values[uid_type]))	
			except:
				logger_main.info("Unknown UID TYPE")	
			logger_main.info("UID->"+str(list_UID))	 		

			return 1 
		else :
			return 0

	#function used to activate ISO/DEP ISO14443-4 data exchange speed 
	# Allowed values 106 kbps / 212 kbps /424 kbps			
	def configure_PPS (self,val_sp): 			
		speed=[0x00,0x01,0x02]
		#speed[0] - >106 kbps
		#speed[1] - >212 kbps
		#speed[2] - >424 kbps
		
		if(val_sp>2 or val_sp<0):
			val_sp=0
			logger_main.info("Default speed Configuration ISO14443-4")

		val_sp_dict={0:"106kbps",1:"212kbps",2:"424kbps"}
		logger_main.info("ISODEP Speed"+val_sp_dict[val_sp])
		PPS=send=self.adafruit_pn532.call_function(_COMMAND_INPSL,params=[0x01,speed[val_sp],speed[val_sp]])




	#function used to echange RAW data APDU with PCD	
	def write_apdu(self,apdu):
		logger_main.info("APDU->Request"+str(apdu))
		send=self.adafruit_pn532.call_function(_COMMAND_INDATAEXCHANGE,params=[0x01]+apdu,response_length=255)
		response=[]
		if (send):
			for i in range(0,len(send)):

				response.append(send[i])
				
			logger_main.info("APDU<-Response:"+str(response)) 			


class board_manager_PICC():
	#create new NFC PCD socket,
	def __init__(self):
		logger_main.info("Socket created - ISO14443 Type A PICC")
		self.adafruit_pn532=NFC_setup.initializare()


	#check firmware version and the connection	
	def get_firmware_version(self):	
		return self.adafruit_pn532.firmware_version

	#config SAM on chipset	
	def config(self):
		self.adafruit_pn532.SAM_configuration()


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
		logger_main.info("RATS is :"+str(connection_response));




	#function used to get data from  a PCD 	
	def PICC_GET_DATA(self):
		get_data=self.adafruit_pn532.call_function(_COMMAND_TGGETDATA,response_length=255)
		logger_main.info(get_data)
		if get_data :
			return 1
		else :
			return 0
	
	#function used to get data to  a PCD 			
	def PICC_SET_DATA(self , data ) :
		set_data=self.adafruit_pn532.call_function(_COMMAND_TGSETDATA,params=data,response_length=255)




#program entry point 

if __name__=="__main__":
#logger SETTINGS

# --------------------------------------------------------------FILE LOGGER SETTINGS --------------------------------------------------------------------------------------------------------------------------------------------
#In Python's logging module, the severity levels are ranked hierarchically from least severe to most severe. Here's the ranking from lowest to highest:

#DEBUG: Detailed information, typically of interest only when diagnosing problems.

#INFO: Confirmation that things are working as expected. Typically used for general information about the program's execution.

#WARNING: Indication that something unexpected happened or an issue might arise in the future, but the program can still continue execution.

#ERROR: Indication of a more serious problem that has occurred during the program's execution. The program may not be able to continue running properly after an error occurs.

#CRITICAL: Indication of a critical error that requires immediate attention. This level is reserved for very severe errors that may lead to the termination of the program.


	logger_main = logging.getLogger("NFC.PY")


# SET DEBUG LEVEL -> ERROR WARNING DEBUG INFO


	logger_main.setLevel(logging.DEBUG)

	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	console_handler.setFormatter(formatter)  # Corrected: Set formatter for the handler

# Add the console handler to the logger
	logger_main.addHandler(console_handler)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


																
	#------------------------------------------------------------------------------------- ISO14443 Type A  PICC 
	#Set MANAGER - AVAILABLE FOR PICC 
	#board_manager=board_manager_PICC()
	#logger_main.info("Board Version - PN532 - {A} ".format(A=board_manager.get_firmware_version()))
	#board_manager.config()


	#------------------------------------------------------------------------------------- ISO14443 Type A  PCD
	#Set MANAGER - AVAILABLE FOR PCD
	#board_manager=board_manager_PCD()
	#logger_main.info("Board Version - PN532 - {A} ".format(A=board_manager.get_firmware_version()))
	#board_manager.config()

	#-------------------------------------------------------------------------------------  MIFARE CLASSIC PCD
	#Set MANAGER - AVAILABLE FOR MIFARE CLASSIC PCD 
	board_manager=board_manager_MIFARE()
	logger_main.info("Board Version - PN532 - {A} ".format(A=board_manager.get_firmware_version()))
	board_manager.config()
	key = b"\xFF\xFF\xFF\xFF\xFF\xFF"


	#loop
	while(True):


		#------------------------------------------------------------------------------------- ISO14443 Type A  PICC 
		#CONFIG AS PICC


		#config_PICC=board_manager.config_PICC()		
		#data=board_manager.PICC_GET_DATA()
		#if data:
		#	board_manager.PICC_SET_DATA([0x90,0x00])


		#------------------------------------------------------------------------------------- ISO14443 Type A  PCD
		#CONFIG AS PCD


		#card_status=board_manager.enlist_target()		
		# SEND APDU
		#logger_main.debug("--------")
		#if(card_status):
		#	#CONFIG PPS
		#	board_manager.configure_PPS(2)
			 
			#WRITE APDU
			#board_manager.write_apdu([0x23,0x49])
		#	board_manager.write_apdu([0x00,0xA4,0x04,0x00,0x10,0xA0,0x00,0x00,0x06,0x04,0x53,0x6D,0x61,0x72,0x74,0x4B,0x65,0x79,0x00,0x01,0x01])
		#time.sleep(1)

		#-------------------------------------------------------------------------------------  MIFARE CLASSIC PCD
		#Set MANAGER - AVAILABLE FOR MIFARE CLASSIC PCD 
		logger_main.debug("--------")
    	# Check if a card is available to read
		uid = board_manager.read_passive_target(timeout=0.5)
		if uid != None :
			logger_main.info("Card logged with uid " + str(uid))
    	# Try again if no card is available.

    	#Write - read a block 
		#if uid is not None:
			

			print("Found card with UID:", [hex(i) for i in uid])
			print("Authenticating block 4 ...")

			board_manager.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)

		# Set 16 bytes of block to 0xFEEDBEEF
		#	data = bytearray(16)
		#	data[0:16] = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


		#Perform authentication
		#board_manager.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)

		# Write 16 byte block.
		#	board_manager.mifare_classic_write_block(4, data)
		# Read block #6
		#	logger_main.info("Wrote to block 4, now trying to read that data:"+str(board_manager.mifare_classic_read_block(4)))
		#	break

		#time.sleep(1)


		#Configure a block to be value block
		#if uid is not None :
			#Perform authentication
		#	board_manager.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
		#	board_manager.mifare_classic_fmt_value_block(4,1)
		#	break

		#Perform actions on value block	
		if uid is not None :
			
			board_manager.mifare_classic_add_value_block(4,50)
			board_manager.mifare_classic_get_value_block(4)
			board_manager.mifare_classic_sub_value_block(4,20)
			board_manager.mifare_classic_get_value_block(4)

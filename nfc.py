import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
import time



from adafruit_pn532.adafruit_pn532 import _COMMAND_INDATAEXCHANGE
from adafruit_pn532.adafruit_pn532 import _COMMAND_INLISTPASSIVETARGET
from adafruit_pn532.adafruit_pn532 import _COMMAND_INPSL

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


#board manager - created for lol lvl interaction with the board
class board_mngr():
	
	#create new NFC socket
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


	#function used to activate ISO/DEP ISO14443-4 data exchange speed 
	# Allowed valies 106 kbps / 212 kbps /424 kbps			
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

#Set Up
board_manager=board_mngr()
print(board_manager.get_firmware_version())
board_manager.mifare_config()

#loop
while(True):
	card_status=board_manager.enlist_target()
	
	if(card_status):
		board_manager.configure_PPS(2)
		board_manager.write_apdu([0x00,0xA4,0x04,0x00,0x10,0xA0,0x00,0x00,0x06,0x04,0x53,0x6D,0x61,0x72,0x74,0x4B,0x65,0x79,0x00,0x01,0x01])
	time.sleep(1)

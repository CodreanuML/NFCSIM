import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

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
		print("Socket set up to be compatible with MIfare Card")

	#return bytecode - raw hex
	def get_raw_UID(self):
		UID=self.adafruit_pn532.read_passive_target(timeout=0.5)
		if (UID!=None):
			print(len(UID))
			return UID
		else :
			return("Card Not Detected") 


	def get_UID(self):
		UID=self.adafruit_pn532.read_passive_target(timeout=0.5)
		list_UID=[]
		if (UID!=None):
			for i in range(0,len(UID)):
				list_UID.append(UID[i])
			
			return list_UID
		else:
			return("Card Not Detected")		

	

#program entry point 

#Set Up
board_manager=board_mngr()
print(board_manager.get_firmware_version())
board_manager.mifare_config()

#loop
while(True):
	print(board_manager.get_raw_UID())

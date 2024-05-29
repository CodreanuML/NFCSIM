import PN532_M as nfc
from machine import Pin, SPI

# SPI
#spi_dev = SPI(0, baudrate=1000000)
#cs = Pin(16, Pin.OUT)
#cs.on()

# SENSOR INIT
#pn532 = nfc.PN532(spi_dev,cs)
#ic, ver, rev, support = pn532.get_firmware_version()
#print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
#pn532.SAM_configuration()

# IMPORRT COMMANDS FOR ISO14443 Type A PCD"

_COMMAND_INDATAEXCHANGE=0x40 
_COMMAND_INLISTPASSIVETARGET=0x4A
_COMMAND_INPSL=0x4E

#IMPORT COMMANDS FOR ISO14443 Type A PICC"

_COMMAND_TGINITASTARGET=0x8C
_COMMAND_TGRESPONSETOINITIATOR=0x90
_COMMAND_TGGETDATA=0x86
_COMMAND_TGSETDATA=0x8E


#Mifare Commands
MIFARE_CMD_AUTH_A = const(0x60)
MIFARE_CMD_AUTH_B = const(0x61)
MIFARE_CMD_READ = const(0x30)
MIFARE_CMD_WRITE = const(0xA0)
MIFARE_CMD_TRANSFER = const(0xB0)
MIFARE_CMD_DECREMENT = const(0xC0)
MIFARE_CMD_INCREMENT = const(0xC1)
MIFARE_CMD_STORE = const(0xC2)
MIFARE_ULTRALIGHT_CMD_WRITE = const(0xA2)



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
            cls.spi=SPI(0, baudrate=1000000)
            cls.cs_pin=Pin(16, Pin.OUT)
            cls.cs_pin.on()
            cls.cip=nfc.PN532(cls.spi,cls.cs_pin)
            cls.count+=1
            return cls.cip
        else:
            return cls.cip
        
#board manager - created for low lvl interaction with NFC board - >>> used when board is set up as PCD (reader/Writer) - > Mifare Classic Version
class board_manager_MIFARE():
    #create new NFC PCD socket,
    def __init__(self):
        print("Socket created - Mifare classic")
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
            print("Key block successfully logged !")
        else:
            print("Key block login failed ! ")

    #read block
    def mifare_classic_read_block(self, block_number: int):  
        read_value =self.adafruit_pn532.mifare_classic_read_block(block_number)
        if read_value==None :
            print("Block not read !")
        else : 
            return read_value

    #write block
    def mifare_classic_write_block(self, block_number: int, data) -> bool:
        write_value = self.adafruit_pn532.mifare_classic_write_block(block_number,data)
        if write_value :
            print("Block successfully written")
        else :
            print("Block writing failed !")

    #format a block to be a value block
    def mifare_classic_fmt_value_block(self, block_number: int, initial_value: int, address_block: int = 0) -> bool:
        status =self.adafruit_pn532.mifare_classic_fmt_value_block(block_number,initial_value)
        if status :
            print("Block number {no} successfully formated to value block !" .format(no=block_number))
        else :
            print("Block number {no} formatation to value block failed ! " .format(no=block_number))

    #return a value block value
    def mifare_classic_get_value_block(self, block_number: int) -> int:
        get_result = self.adafruit_pn532.mifare_classic_get_value_block(block_number)
        print("Block number " + str(block_number) + " has value " + str(get_result))

    #subtract a value from a value block
    def mifare_classic_sub_value_block(self, block_number: int, amount: int) -> bool:
        substraciton_result=self.adafruit_pn532.mifare_classic_sub_value_block(block_number,amount)
        if substraciton_result :
            print("Block number {no} successfully decreased with value {value} !".format(no=block_number,value=amount))
        else :
            print("Substraction failed ! ")

    #add a value to a value block
    def mifare_classic_add_value_block(self, block_number: int, amount: int) -> bool:
        add_result=self.adafruit_pn532.mifare_classic_add_value_block(block_number,amount)
        if add_result :
            print("Block number {no} successfully incresed with value {value} !".format(no=block_number,value=amount))
        else:
            print("Adition failed !")



#board manager - created for low lvl interaction with NFC board - >>> used when board is set up as PCD (reader/Writer)
class board_manager_PCD():
    
    #create new NFC PCD socket,
    def __init__(self):
        print("Socket created - ISO14443 Type A PCD")

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
            print("Card Enlisted")
            for i in range(0,len(enlisted_UID)):

                list_UID.append(enlisted_UID[i])
                uid_type=len(list_UID)//3
            try: 
                print("UID Type -> {uidtype}".format(uidtype=uid_values[uid_type]))	
            except:
                print("Unknown UID TYPE")
            print("UID->"+str(list_UID))

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
            print("Default speed Configuration ISO14443-4")

        val_sp_dict={0:"106kbps",1:"212kbps",2:"424kbps"}
        print("ISODEP Speed"+val_sp_dict[val_sp])
        PPS=send=self.adafruit_pn532.call_function(_COMMAND_INPSL,params=[0x01,speed[val_sp],speed[val_sp]])




    #function used to echange RAW data APDU with PCD
    def write_apdu(self,apdu):
        print("APDU->Request"+str(apdu))
        send=self.adafruit_pn532.call_function(_COMMAND_INDATAEXCHANGE,params=[0x01]+apdu,response_length=255)
        response=[]
        if (send):
            for i in range(0,len(send)):

                response.append(send[i])

            print("APDU<-Response:"+str(response)) 


class board_manager_PICC():
#create new NFC PCD socket,
    def __init__(self):
        print("Socket created - ISO14443 Type A PICC")
        self.adafruit_pn532=NFC_setup.initializare()


    #check firmware version and the connection
    def get_firmware_version(self):
        return self.adafruit_pn532.firmware_version

    #config SAM on chipsets
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
        print("RATS is :"+str(connection_response));




    #function used to get data from  a PCD 
    def PICC_GET_DATA(self):
        get_data=self.adafruit_pn532.call_function(_COMMAND_TGGETDATA,response_length=255)
        print(get_data)
        if get_data :
            return 1
        else :
            return 0

    #function used to get data to  a PCD 
    def PICC_SET_DATA(self , data ) :
        set_data=self.adafruit_pn532.call_function(_COMMAND_TGSETDATA,params=data,response_length=255)


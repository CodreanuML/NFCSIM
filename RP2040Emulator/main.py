import nfc_stack as nfc_stack
import time
import _thread
import sys
import select

from PN532_M import MIFARE_CMD_AUTH_B

#------------------------------------------------------------------------------------- ISO14443 Type A  PICC 
#Set MANAGER - AVAILABLE FOR PICC 
#board_manager=board_manager_PICC()
#print("Board Version - PN532 - {A} ".format(A=board_manager.get_firmware_version()))
#board_manager.config()


#------------------------------------------------------------------------------------- ISO14443 Type A  PCD
#Set MANAGER - AVAILABLE FOR PCD
#board_manager=board_manager_PCD()
#print("Board Version - PN532 - {A} ".format(A=board_manager.get_firmware_version()))
#board_manager.config()

#-------------------------------------------------------------------------------------  MIFARE CLASSIC PCD
#Set MANAGER - AVAILABLE FOR MIFARE CLASSIC PCD 
board_manager=nfc_stack.board_manager_MIFARE()
print("Board Version - PN532 - {A} ".format(A=board_manager.get_firmware_version()))
board_manager.config()
key = b"\xFF\xFF\xFF\xFF\xFF\xFF"


#loop
while(True):


#------------------------------------------------------------------------------------- ISO14443 Type A  PICC 
#CONFIG AS PICC


#config_PICC=board_manager.config_PICC()
#data=board_manager.PICC_GET_DATA()
#if data:
#board_manager.PICC_SET_DATA([0x90,0x00])


#------------------------------------------------------------------------------------- ISO14443 Type A  PCD
#CONFIG AS PCD


#card_status=board_manager.enlist_target()
# SEND APDU
#print("--------")
#if(card_status):
#CONFIG PPS
#board_manager.configure_PPS(2)
 
#WRITE APDU
#board_manager.write_apdu([0x23,0x49])
#board_manager.write_apdu([0x00,0xA4,0x04,0x00,0x10,0xA0,0x00,0x00,0x06,0x04,0x53,0x6D,0x61,0x72,0x74,0x4B,0x65,0x79,0x00,0x01,0x01])
    time.sleep(1)

#-------------------------------------------------------------------------------------  MIFARE CLASSIC PCD
#Set MANAGER - AVAILABLE FOR MIFARE CLASSIC PCD 
    print("--------")
# Check if a card is available to read
    uid = board_manager.read_passive_target(timeout=0.5)
    if uid != None :
        print("Card logged with uid " + str(uid))
# Try again if no card is available.

#Write - read a block 
#if uid is not None:


        print("Found card with UID:", [hex(i) for i in uid])
        print("Authenticating block 4 ...")

#        board_manager.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)

# Set 16 bytes of block to 0xFEEDBEEF
#data = bytearray(16)
#        data[0:16] = b"\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

#Perform authentication
#board_manager.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)

# Write 16 byte block.
#        board_manager.mifare_classic_write_block(4, data)
# Read block 
#        print("Wrote to block 4, now trying to read that data:"+str(board_manager.mifare_classic_read_block(4)))
#break

#        time.sleep(1)


#Configure a block to be value block
#    if uid is not None :
#Perform authentication
        board_manager.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
        #board_manager.mifare_classic_fmt_value_block(4,1)
        #break

#Perform actions on value block
    #if uid is not None :

        board_manager.mifare_classic_add_value_block(4,50)
        board_manager.mifare_classic_get_value_block(4)
        #board_manager.mifare_classic_sub_value_block(4,20)
        #board_manager.mifare_classic_get_value_block(4)

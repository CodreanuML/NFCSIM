import nfc_stack as nfc_stack
  
#enter point for our program :


pn532 = nfc_stack.NFC_setup.initializare()
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
while True :
    pass 

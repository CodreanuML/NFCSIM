import PN532_M as nfc
from machine import Pin, SPI

# SPI
spi_dev = SPI(0, baudrate=1000000)
cs = Pin(16, Pin.OUT)
cs.on()

# SENSOR INIT
pn532 = nfc.PN532(spi_dev,cs)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()
  
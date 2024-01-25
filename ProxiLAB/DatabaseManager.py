import json

class Database():


	_smoke_DB={

		
		"ATQA":[0x04,0x03],
		"ATS":[0x0A,0x78,0x77,0x91,0x02,0x80,0x73,0xc8,0x21,0x10],
		"UID_TYPE":1,
		"UID_LEN":10,
		"UID":[0x88,0x04,0x57,0x23,0xF8,0xBA,0x39,0x13,0x90,0x00,0x73,0xC8,0x21,0x10],
		"DESELECT":[0xC2],
		"SWTX":[0xF2,0x01],
		"SAKI":[0x24],
		"SAKC":[0x20],
		"Nr_APDU":2,
		"APDU1":{"Req":[0x23,0x49],
				 "Resp":[0x55]		},
		"APDU2":{"Req":[0x22,0x42],
				 "Resp":[0x55]		},		 






		}

	def __init__(self,cardtype):
		print("Socket to Database created.")
		#cardtype values  : 1 = ISO 14443 4A
		#                   2 = ISO 14443 4B
		if cardtype==1 or cardtype==2:    					
			self.emulatedcard=cardtype
		else:
			self.emulatedcard=1
			print("Cardtype set to default ")	
	def write_to_db_smoke(self):	
		with open("ProxiLABdatabase_Type4A.json", "w") as write_file:
    			json.dump(self._smoke_DB, write_file)

	def read_db(self):
		with open("ProxiLABdatabase_Type4A.json", "r") as read_file:
			data = json.load(read_file)
		return data





if __name__ == "__main__":
	Db_socket=Database(1)
	Db_socket.write_to_db_smoke();
	data=Db_socket.read_db();
	


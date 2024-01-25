

import sys
import site
import os
site.addsitedir( os.environ['RGPA_PATH'] + '..\\Quest\\Lib' )

import win32com.client
import pythoncom
import sys
import ctypes
import time

from DatabaseManager import Database


class APDU():
    request=None
    response=None

    def __init__(self,request,response):
        self.request=request
        self.response=response


class Manager():
    #creating a new database socket Database(val : 1-Type 4a , 2-Type 4b)
    _cardtype= 1
    _DatabaseManager=None
    _database=None
    _ProxiLAB=None
    _NrApdu=0
    APDUS=[]
    def __init__(self,card_type,ProxiLAB):

        if card_type==1 or card_type==2 :
            self._cardtype=card_type
        else :
            self._cardtype=1

        self._DatabaseManager=Database(self._cardtype)    
        self._ProxiLAB=ProxiLAB
    def Settings(self):

        if self._cardtype==1:

            self._database=self._DatabaseManager.read_db()    
            print(self._database)
            ATQA=self._database["ATQA"]
            ATS=self._database["ATS"]
            UID=self._database["UID"]
            DESELECT=self._database["DESELECT"]
            SWTX=self._database["SWTX"]
            SAKI=self._database["SAKI"]
            SAKC=self._database["SAKC"]
            UID_Type=self._database["UID_TYPE"]
            UID_LEN=self._database["UID_LEN"]
            self._NrApdu=self._database["Nr_APDU"]
            self._ProxiLAB.Settings.Mode = ProxiLABUtilities.Constants.MODE_EMULATOR_A_B
            #ProxiLAB.Emulator.ISO14443.TypeA.LoadDefaultConfig()  
            self._ProxiLAB.Emulator.ISO14443.LoadSDeselect(DESELECT)
            self._ProxiLAB.Emulator.ISO14443.LoadSWTX(SWTX)
            self._ProxiLAB.Emulator.ISO14443.TypeA.LoadATQA(ATQA)
            self._ProxiLAB.Emulator.ISO14443.TypeA.UIDType=UID_Type
            self._ProxiLAB.Emulator.ISO14443.TypeA.UIDLength=UID_LEN
            self._ProxiLAB.Emulator.ISO14443.TypeA.LoadUID(UID)
            self._ProxiLAB.Emulator.ISO14443.TypeA.LoadATS(ATS)
            self._ProxiLAB.Emulator.ISO14443.TypeA.LoadSAKI(SAKI)
            self._ProxiLAB.Emulator.ISO14443.TypeA.LoadSAKC(SAKC)
            self._ProxiLAB.Emulator.ISO14443.TypeA.Enable = 0


            for i in range(1,self._NrApdu+1): 

                new_APDU=APDU(self._database["APDU"+str(i)]["Req"],self._database["APDU"+str(i)]["Resp"])
                print(self._database["APDU"+str(i)]["Req"])
                self.APDUS.append(new_APDU)

        else :

            print("Type4b Not implemented")







def Test(proxilab):
    err = 0
    count = 0
    
    
    ProxiLAB.Emulator.ISO14443.TypeA.Enable = 1
    
    while(err==0):
        #Wait for a PCD frame
        request = ProxiLABUtilities.CreateVARIANT()
        
        err = ProxiLAB.Emulator.ISO14443.WaitAndGetFrame(1000, request)
        #err=ProxiLAB.Emulator.ISO14443.WaitAndGetFrameStatus(1000)
        if(err[0]==0):
            err = ProxiLAB.Emulator.ISO14443.SendFrame(2000, [0x72,0xEC])
            count += 1
        #No frame received: keep on waiting
        elif((err[0] == ProxiLABUtilities.Constants.ERR_TIMEOUT) or (err[0] == ProxiLABUtilities.Constants.ERR_EMU_NO_FRAME_AVAILABLE)):
            err = 0
            count +=1
       
        if(count == 10):
                ProxiLAB.Emulator.ISO14443.TypeA.Enable = 0
                return




#Main function
def Main(proxilab):
    
    #Test settings
    Manag=Manager(1,ProxiLAB) 
    Manag.Settings()

    #Start the trace
    ProxiLABUtilities.StartSpy(proxilab)
    #ProxiLAB.Emulator.ISO14443.TypeA.Enable = 1
    #Application
    Test(proxilab)
    #time.sleep(20)
    #Stop the trace module
    ProxiLAB.Emulator.ISO14443.TypeA.Enable = 0
    ProxiLABUtilities.StopSpy(proxilab)
    
















#PROGRAM ENTRY POINT
    
if __name__ == "__main__":
    #Create and check connection ----- >>>>>>> Create a new connection and load default configurations <<<<<<< ---------------

    # Create ProxiLAB COM object - create a new connection
    ProxiLAB = win32com.client.Dispatch("KEOLABS.ProxiLAB")

    # Test if ProxiLAB is connected
    if (ProxiLAB.IsConnected==0):
        print("Connection Failed!-Check your ProxiLAB connection. ProxiLAB is not connected to your PC!")
    else:  
        # Import constants values
        sys.path.append(ProxiLAB.GetToolDirectory() + '\inc')
        import ProxiLABUtilities
    
        # Reset ProxiLAB's configuration
        ProxiLAB.Settings.LoadDefaultConfig()

        #Clear RGPA Output view
        ProxiLAB.Display.ClearOutput()
    





        #Call main function ----- >>>>>>> IN MAIN ARE ALLL MAIN FUNCTIONS CALLLED <<<<<<< ---------------
        Main(ProxiLAB)
    




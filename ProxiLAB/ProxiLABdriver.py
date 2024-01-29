

import sys
import site
import os
site.addsitedir( os.environ['RGPA_PATH'] + '..\\Quest\\Lib' )
import win32com.client
import pythoncom
import sys
import ctypes
import time
import logging
from DatabaseManager import Database




logginglvls={"WARNING":logging.WARNING,
"DEBUG":logging.DEBUG,
"INFO":logging.INFO,
"WARNING":logging.WARNING,
"ERROR":logging.ERROR,
"CRITICAL":logging.CRITICAL}

#filename="ProxiLABdriverLogger.log"

logging.basicConfig(level=logginglvls["DEBUG"])





class APDU():
    _request=None
    _response=None

    def __init__(self,request,response):
        self._request=request
        self._response=response


    def getrequest(self):
        return self._request

    def getresponse(self):
        return self._response


class EmulationManager():
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

    def LoadSDeselect(self,DESELECT):
        self._ProxiLAB.Emulator.ISO14443.LoadSDeselect(DESELECT)

    def LoadSWTX(self,SWTX):             
        self._ProxiLAB.Emulator.ISO14443.LoadSWTX(SWTX)


    def LoadATQA(self,ATQA):
        self._ProxiLAB.Emulator.ISO14443.TypeA.LoadATQA(ATQA)


    def UIDType(self,UID_Type):
        self._ProxiLAB.Emulator.ISO14443.TypeA.UIDType=UID_Type

    def UIDLength(self,UID_LEN):
        self._ProxiLAB.Emulator.ISO14443.TypeA.UIDLength=UID_LEN

    def LoadUID(self,UID):     
        self._ProxiLAB.Emulator.ISO14443.TypeA.LoadUID(UID)

    def LoadATS(self,ATS):
        self._ProxiLAB.Emulator.ISO14443.TypeA.LoadATS(ATS)

    def LoadSAKI(self,SAKI):
        self._ProxiLAB.Emulator.ISO14443.TypeA.LoadSAKI(SAKI)

    def LoadSAKC(self,SAKC):
        self._ProxiLAB.Emulator.ISO14443.TypeA.LoadSAKC(SAKC)

    def Enable(self):
        self._ProxiLAB.Emulator.ISO14443.TypeA.Enable = 1

    def Disable(self):
        self._ProxiLAB.Emulator.ISO14443.TypeA.Enable = 0

    def GetDatabaseManager(self) -> Database :
        return self._DatabaseManager

    def GetNrApdu(self) -> int :
        return self._NrApdu

    def GetAPDUS(self) -> list :
        return self.APDUS

    def Settings(self):

        if self._cardtype==1:

            self._database=self._DatabaseManager.read_db()    
            logging.debug(self._database)
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
                self.APDUS.append(new_APDU)

        else :

            logging.debug("Type4b Not implemented")


class Connection():

    _COM=None
    def __init__(self):
        logging.debug("New Connection established")

    def create_connection(self):
        # Create ProxiLAB COM object - create a new connection
        self._COM=win32com.client.Dispatch("KEOLABS.ProxiLAB")

    def connect(self):
        # Test if ProxiLAB is connected
        if (self._COM.IsConnected==0):
            logging.debug("Connection Failed!-Check your ProxiLAB connection. ProxiLAB is not connected to your PC!")
            return 0
        else:  
            # Import constants values

            
            # Reset ProxiLAB's configuration
            self._COM.Settings.LoadDefaultConfig()

            #Clear RGPA Output view
            self._COM.Display.ClearOutput()
            return 1
    


    def get_COM(self):
        return self._COM

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
            err = ProxiLAB.Emulator.ISO14443.SendFrame(2000, [0x90,0x00])
            count += 1
        #No frame received: keep on waiting
        elif((err[0] == ProxiLABUtilities.Constants.ERR_TIMEOUT) or (err[0] == ProxiLABUtilities.Constants.ERR_EMU_NO_FRAME_AVAILABLE)):
            err = 0
            count +=1
       
        if(count == 10):
                ProxiLAB.Emulator.ISO14443.TypeA.Enable = 0
                return


class Emulation ():
    _err=0
    _count=0

    ProxiLAB=None
    manager=None
    def __init__(self,proxilab,manager : EmulationManager):
        logging.info("Emulator created")
        self.ProxiLAB=proxilab
        self.manager=manager


    def find_APDU(self,req : list ) -> list :
        APDUS=self.manager.GetAPDUS()
        for apdu in APDUS :
            if apdu.getrequest() == req :
                return apdu.getresponse()
        else :
            logging.debug("return 404")
            return ["404"]  # APDU RESPONSE FOR NOT IMPLEMENTED REQ

    def emulate(self): 
        self.manager.Enable()
        while(self._err==0):
            #Wait for a PCD frame
            request = ProxiLABUtilities.CreateVARIANT()
        
            self._err = self.ProxiLAB.Emulator.ISO14443.WaitAndGetFrame(1000, request)
            #err=ProxiLAB.Emulator.ISO14443.WaitAndGetFrameStatus(1000)
            if(self._err[0]==0):
                request=list(self._err[1])
                response=self.find_APDU(request)
                if(response!=["404"]):
                    self._err = self.ProxiLAB.Emulator.ISO14443.SendFrame(1000, response)
                    self._count += 1
                else:
                    self._count += 1
                    self._err=self.ProxiLAB.Emulator.ISO14443.SendFrame(1000, [0x90,0x00])
            #No frame received: keep on waiting
            elif((self._err[0] == ProxiLABUtilities.Constants.ERR_TIMEOUT) or (self._err[0] == ProxiLABUtilities.Constants.ERR_EMU_NO_FRAME_AVAILABLE)):
                self._err = 0
                self._count +=1
       
            if(self._count == 10):
                self.ProxiLAB.Emulator.ISO14443.TypeA.Enable = 0
                return


#Main function
def Main(proxilab,manager,emulator):
    manager.Settings()
    #Start the trace
    ProxiLABUtilities.StartSpy(proxilab)
    #ProxiLAB.Emulator.ISO14443.TypeA.Enable = 1
    #Application
    #Test(proxilab)
    emulator.emulate()
    #time.sleep(20)
    #Stop the trace module
    ProxiLAB.Emulator.ISO14443.TypeA.Enable = 0
    ProxiLABUtilities.StopSpy(proxilab)
    



#PROGRAM ENTRY POINT
    
if __name__ == "__main__":
    #Create and check connection ----- >>>>>>> Create a new connection and load default configurations <<<<<<< ---------------

    
    # Create ProxiLAB COM object - create a new connection
#    ProxiLAB = win32com.client.Dispatch("KEOLABS.ProxiLAB")

    # Test if ProxiLAB is connected
#    if (ProxiLAB.IsConnected==0):
#        print("Connection Failed!-Check your ProxiLAB connection. ProxiLAB is not connected to your PC!")
#    else:  
        # Import constants values
#        sys.path.append(ProxiLAB.GetToolDirectory() + '\inc')
#        import ProxiLABUtilities
    
        # Reset ProxiLAB's configuration
#        ProxiLAB.Settings.LoadDefaultConfig()

        #Clear RGPA Output view
#        ProxiLAB.Display.ClearOutput()
    
    logging.info("EMULATOR STARTED")
    ProxiConnection=Connection()
    ProxiConnection.create_connection()
    Connection_status=ProxiConnection.connect()
    ProxiLAB=ProxiConnection.get_COM()
    if Connection_status==0 : 
        pass
    else :
        sys.path.append(ProxiLAB.GetToolDirectory() + '\inc')
        import ProxiLABUtilities

    Manag=EmulationManager(1,ProxiLAB)
    Emulator=Emulation(ProxiLAB,Manag)
        #Call main function ----- >>>>>>> IN MAIN ARE ALLL MAIN FUNCTIONS CALLLED <<<<<<< ---------------
    Main(ProxiLAB,Manag,Emulator)
    




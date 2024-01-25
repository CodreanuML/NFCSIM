

#Import modules
import win32com.client
import time
import sys

#Create ProxiSPY object
ProxiSPY = win32com.client.Dispatch("KEOLABS.ProxiSPY")

#Create WshShell object to get My Documents path
WshShell = win32com.client.Dispatch("Wscript.Shell")

#Restore default settings
ProxiSPY.Settings.LoadDefaultConfig()

ProxiSPY.Spy.Log.OutputBinaryFile = r"C:\LOG\ProxySpy.log"

def Main():
       
    #Capture some frames
    print ("Acquiring...")
    error = ProxiSPY.Spy.Start()
    if error:
        print ("Failed to start trace!")
        return
    time.sleep(3)


    #Perform protocol analysis
    print ("Analyzing...")
    error = ProxiSPY.Spy.Log.Start()
    if error:
        print ("Failed to start analysis!")
        return
    
    time1=time.time()
    delta_t=0
    time_to_search=30
    word=[]
    answer = []
    answer_str = ""
    while(delta_t<time_to_search):
        

    #GetFrame - 1: Perform the GetFrame and retrieve the status
        err = ProxiSPY.Spy.Log.GetFrameStatus()
    #Check status
        if not err:
    #GetFrame – 2: Retrieve the frame as a string (ONLY IF err IS NULL!)
            answer_str = ProxiSPY.Spy.Log.GetFrameStr()
    #Convert the string into an array
            answer.append(answer_str)
    #GetFrame – 3: Retrieve the frame type
            frameType = ProxiSPY.Spy.Log.GetFrameType()
        delta_t=time.time()-time1        

    #Wait for the end of analysis
    error = ProxiSPY.Spy.Log.Stop()
    if error:
        print ("Failed to wait for the end of analysis!")
        return
   
    error = ProxiSPY.Spy.Stop()
    if error:
        print ("Failed to stop trace!")
        return      
    with open("C:\LOG\ProxySpy.log", 'rb') as file:
        binary_data=file.read()
        print(binary_data)
    
    print(answer)
    with open("C:\LOG\ProxySpy_file.txt", 'w') as file:
    	for i in answer :
        	binary_data=file.write(i+'\n')
    ProxiSPY.Spy.Analyzer.Start()	
#Call main function
Main()
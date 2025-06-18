#def greet(name0, adifCont, rxExch) :
    
    
#    if "class" in adifCont[11:16] :   #0
#        rxExc1 = rxExch
        #echo = input("rxE")
#        return  [rxExc1]
    
#    if "arrl_" in adifCont[21:26] :  
#        rxExc2 = rxExch
#        return  [rxExc2]
    
#    if "SPC2 " in adifCont[31:36] :  
#        rxExc3 = rxExch 
#        return  [rxExc3]

    
#    print("Hello, " + name0 )
    #echo = input("greet")
#   gave up on functions working for me    

    






# Convert adif file to cabrillo
#the starting point base code for this app was provided by  AA6XA jeff:
#<https://github.com/kabelj/Adif2Cabrillo/blob/main/adif2cabrillo.py>
#further developement for the general use case: ki4ezc fred
# see my support help "pythonConvertReadMe.pdf"
# change log
#     12/4/2024  initial beta testing ready to share
#     12/20/2024 appended counts for qso, domestic calls, unique states unique countries
#     12/21/2024 append addition of no dupes
#     12/22/2024 handles UPPER and lower case adif to meet standard
#                added switch for horizontal vrs vertical input adi format
#     01/23/2025 broke out RY mode default from digital for RTTY
#     04/14/2025 fixed freq formating truncation when freq nn.nnn format
#     04/13/2025 all qso rows must be uppercase
#     04/14/2025 append addition for no dupes if in his exchange only
#     04/27/2025 added sum qso s by band 160m - 2m
#                fixed length of freq to b wwddd (flagged by FL QP when ddddd)
#     05/05/2025 append addition of unique exchange (connts unique counties on QPs)
#     05/10/2025 append possible callsign error (not found qrz)
#     05/20/2025 on (serial stx): pads leading "0" to fill length = 3
#     05/23/2025 append list of their unique call sign prefixs
#     05/29/2025 append contest and adifCont value to summary
#     05/30/2025 append estimated error rate
#     06/01/2025 1)execution controls CVinputForm___.txt 2)adif input file picked using windows dialog box
#     06/05/2025 added "4 county" input capable
#     06/11/2025 3 value positional started

noQSO =0
noDom =0
noState=0
noContry =0

noUniExch =0
noBustedExchg =0
noLikeError =  0
noErrorRate = 0.0
        
nPrefix  =0
nNoName =0


noB160 =0
noB80 =0
noB40 =0
noB20 =0
noB15 =0
noB10 =0
noB6 =0
noB2 =0


cContest = "none"
cAccumSt=""
cAccumCty=""
cAccumUniExch= "none"
cTestUniExch= ""
cNameFound = "nd"
cNoNameList = "none  "
cAccumPrefix = ""


myCountry= "United States"  
#*******************
cHorizontalFormat = "N"
#*******************
cQCBsingle =""

cQCBTestlist =""
cQCBDupelist = "none"
noDupe =0


cQCBDupeExchgTestlist = ""
cQCBDupeExchglist = "none"
noDupeExchg =0

cFoundCountry = "N"
cFoundState = "Y"

rxExc1 = ""
rxExc2 = ""
rxExc3 = ""

myExchangePostfix = ""

#*******************
#import dingsound



import tkinter as tk
from tkinter import filedialog
echo = print ("PICK CV INPUT")
def pick_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path

if __name__ == '__main__':
    selected_file = pick_file()
    if selected_file:
        print(f"Selected file: {selected_file}")
        adifControl = selected_file
    else:
        print("No file selected")


iError = -1 # -1 no error
    
  
fControl = open(adifControl, 'r')
#echo = input("open")
controlEntries = fControl.readlines()
nothing =0
cAccumToken = ""
cValFound = 0

myCall = "nd"
mySection = "nd"
myState = "nd"
catBand = "nd"
catPower = "nd"
catMode = "nd"
createdBy = "nd"
myName = "nd"
contest = "nd"




for line in controlEntries:
    controlEntries = fControl.readlines
    
    
    #print(line)
    #echo = input("one read")
    
    if "'" not in line :
        #echo = input ("here")
        nothing =0 # record from control
        #code executed at least once
        # on error produce iError -1
        if cValFound == 0 : #before the 'value' line
            if "@ " in line: #flagged line
                nLen =len(line)-1
                cToken = line[2:nLen]
                cAccumToken = cAccumToken +" " + cToken
            if "value" in line:
                cValFound =1 #found
        else:  #after the 'value' line
            if "@ " in line:
                
                if "CALLSIGN:" in line:
                    nLen =len(line)-1
                    myCall = line [12:nLen]
                    
                if "LOCATION:" in line:
                    nLen =len(line)-1
                    mySection = line [12:nLen]
                    myState = mySection
    
                if "CATEGORY-BAND:" in line:
                    nLen =len(line)-1
                    catBand = line [16:nLen]
    
                if "CATEGORY-POWER:" in line:
                    nLen =len(line)-1
                    catPower = line [18:nLen]
    
                if "CATEGORY-MODE:" in line:
                    nLen =len(line)-1
                    catMode = line [17:nLen]
    
                if "CREATED-BY:" in line:
                    nLen =len(line)-1
                    createdBy = line [14:nLen]
    
                if "NAME:" in line:
                    nLen =len(line)-1
                    myName = line [7:nLen]
              
                if "CONTEST:" in line:
                    nLen =len(line)-1
                    contest = line [11:nLen]
            
        if "myExchangePrefix" in line:
            nLen =len(line)-1
            myExchangePrefix = line[19:nLen]
            if myExchangePrefix != "" :    
                txExch = ""
            
        if "myExchangePostfix" in line:
            nLen =len(line)-1
            myExchangePostfix = line[19:nLen]
            if myExchangePostfix != "" :
                txExch = ""
            
        if "longExch18" in line:
            longExch18 = line[13]
            #echo=input("long")
        
        if "cShowRST" in line:
            cShowRST = line[11]
            
        if "cvSavePath" in line:
            nLen =len(line)-1
            cvSavePath = line[13:nLen]
            #echo = input("path")
    
        if "cHorizontalFormat" in line:
            cHorizontalFormat = line[20]
            #echo =input("for")
    
        iError = -1 #simulated error
    else :
        #print (line)
        nothing = 0
        
    if "<end " in line:
        cPath = cvSavePath+ myCall +".cv"
        file_path = cPath

        #echo = input ("open")
        # Open the file in write mode
        fCab = open(file_path, 'w')
        # Write data to the file
        fCab.write("START-OF-LOG: 3.0\n")
        if contest != "nd" :
            fCab.write("CONTEST: "+contest+"\n")
        if mySection != "nd" :    
            fCab.write("LOCATION: "+mySection+"\n")
        if myCall != "nd" :   
            fCab.write("CALLSIGN: "+myCall+"\n")
        fCab.write("CATEGORY-OPERATOR: SINGLE-OP\n")
        fCab.write("CATEGORY-TRANSMITTER: ONE\n")
        fCab.write("CATEGORY-ASSISTED-NOT ASSISTED: NOT ASSISTED\n")
        if catBand != "nd" :
            fCab.write("CATEGORY-BAND: "+catBand+"\n")
        if catPower != "nd" :    
            fCab.write("CATEGORY-POWER: "+catPower+"\n")
        if catMode != "nd" :    
            fCab.write("CATEGORY-MODE: "+catMode+"\n")
        fCab.write("CATEGORY-STATION: FIXED\n")
        fCab.write("CLAIMED-SCORE: \n")
        if createdBy != "nd" :
            fCab.write("CREATED-BY: "+createdBy+"\n")
        if myName != "nd" :    
            fCab.write("NAME: " + myName + "\n")
        fCab.write("EMAIL:  \n")
        fCab.write("ADDRESS: \n")
        if myCall != "nd" :  
            fCab.write("OPERATORS: "+myCall+"\n")

        print(f"File '{file_path}' created and written successfully.")
        # error checking here
        print ("contr>" + cAccumToken)
        print ("pre  >" + myExchangePrefix)
        print ("post >" + myExchangePostfix)  
        print ("long >" + longExch18) 
        print ("rst  >" + cShowRST)
        print ("==   >  " + cPath)
        print ("cont >" + contest)
      
        nothing =1        
        if iError == 1:
            echo= print("1 finished with error condx")
        else :
            adifCont= cAccumToken
            echo = print ("CV input NO error found")
    
    nothing =2 
    #echo = print ("2")
    
    nothing = 3  #for  
    #echo = print ("3")   

            
echo=print("close")
fControl.close()
#*********************



multstx = "N"
if "(2)"in adifCont or "(3)" in adifCont:
    multstx = "Y"  #first cell of srx_string has length 8
 
#import tkinter as tk
#from tkinter import filedialog
echo = print ("PICK ADI FILE INPUT")
def pick_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path

if __name__ == '__main__':
    selected_file = pick_file()
    if selected_file:
        print(f"Selected file: {selected_file}")
        adifFlnm = selected_file
    else:
        print("No file selected")




    
#adifFlnm = input('Enter Adif filename to read: ')
#cabFlnm = input('Enter Cabrillo filename to write (ki4ezc.cv): ')


#open(adifFlnm, 'r') as fAdif  
fAdif = open(adifFlnm, 'r')
#fCab = open(cabFlnm, 'w')
#echo = input ("open cv")

#contest = input("Contest name: ")

if longExch18== "N":
    fCab.write("XHD: ***** ** yyyy-mm-dd nnnn ************* nnn ****** ************* nnn ****** + \n")
    fCab.write("XHD: freq  mo date       time call          rst exch   call          rst exch   + \n")

if longExch18== "Y":
    fCab.write("XHD: ***** ** yyyy-mm-dd nnnn ************* nnn ****************   ************* nnn ****************** + \n")
    fCab.write("XHD: freq  mo date       time call          rst exch               call          rst exch               + \n")

#  so far 100% buggered up character from copy cwget or foreign address
#echo = input("readfault?next- if fail copy .adi to .txt try agn.") 
#read the entire file
adifEntries = fAdif.readlines()
#echo = input("echo1")
freq = "nd"
band = "nd"
mode = "nd"
date = "nd"
time = "nd"
txExch = "//"
rxExch = "//"
if multstx == "Y":
   txExch = ""
   rxExch = "" 
if myExchangePrefix != "" :    
    txExch = ""
    
print ( txExch)
#echo = input("init")
    
if myExchangePostfix != "" :
    txExch = ""
 
    
    
call = "nd"
rstrx = "599"
rsttx = "599"
if cShowRST == "N":
    rstrx = ""
    rsttx = ""


hisCountry = myCountry
hisState = "nd"

cAccumSt = ""
cAccumCty = ""
  
#echo = input("didnotfail")
#read line by line
for line in adifEntries:
    adifEntries = fAdif.readlines
    #text = "hello world"
    #uppercase_text = text.upper()
    #adifEntries= loweradifEntries.upper() did not work
    #to fix this case must do:if "time_on" in line or  "TIME_ON" in line.upper():
        # about 18 occurs plus several others
    #C:\Users\Owner\.spyder-py3\ki4ezc.100231.20241130234911(1).adi
    #echo = input("echo3")
    #fCab.write(line)

    #only want lines with QSOs
    if cHorizontalFormat == "Y":
        if line[1:5]=="CALL":
            idx = line.find("BAND:")       #idx = line.find("FREQ:")
            numChar = int(line[idx+5+2]) #+2
            freq = line[idx+7:idx+7+numChar]
                                #ii = freq.find(".")
                                #freq = freq[0:ii]+freq[ii+1:ii+4]

            idx = line.find("MODE:")
            numChar = int(line[idx+5])
            mode = line[idx+7:idx+7+numChar]

            idx = line.find("QSO_DATE:")+2
            date = line[idx+11:idx+11+4]+"-"+line[idx+11+4:idx+11+6]+"-"+\
                line[idx+11+6:idx+11+8]

            idx = line.find("TIME_ON:")
            numChar = int(line[idx+8])
            time = line[idx+10:idx+10+numChar]

            idx = line.find("CALL:")
            numChar = int(line[idx+5])
            call = line[idx+7:idx+7+numChar]

            # cabrillo rx exchange
            idx = line.find("SRX_STRING:")
            if idx >0:
                rxExch = line[idx+13:idx+13+numChar]
                numChar = int(line[idx+11])

            # cabrillo tx exchange
            idx = line.find("STX_STRING:")
            if idx >0:
                numChar = int(line[idx+11])
                txExch = line[idx+13:idx+13+numChar]
    
            if cShowRST == "Y":
                nothing =0
          
        
    else:   
        if "<contest" in line or "<CONTEST" in line.upper():
            cContest = line
        
        
        if "time_on" in line or "TIME_ON" in line.upper():
            #<time_on:4>0001
            #01234567890123456
            #echo=input("time_on")
            #idx = line.find("time_on")    #problem for upper case
            numChar = int(line[9])     #not tested
            time = line[11:15]
           
        if "band:" in line or "BAND:" in line.upper():
            #<band:3>20m
            #123456789012
            numChar = int(line[6])
                
            band = line[8:8+numChar]
            #echo=input("band")
            if "160m" in line or "160M" in line.upper():noB160 =noB160+1
            if "80m" in line or "80M" in line.upper():noB80 =noB80+1
            if "40m" in line or "40M" in line.upper():noB40 =noB40+1
            if "20m" in line or "20M" in line.upper():noB20 =noB20 +1
            if "15m" in line or "15M" in line.upper():noB15 =noB15+1
            if "10m" in line or "10M" in line.upper():noB10 =noB10+1
            if "6m" in line or "6M" in line.upper():noB6 =noB6+1
            if "2m" in line or "2M" in line.upper():noB2 =noB2+1
            
        if "freq_rx"in line or "FREQ_RX"in line.upper(): 
            #<freq_rx:2>14
            #123456789012x
            
            numChar = int(line[9])
            #echo= input("freq0")
            if numChar == 1 :
                freq = "0"+ line[11] +"000"
            else:   
                freq = line[11:11+numChar] +"000"
            
            idx = line.find(".")
            #print(str(idx)+"xx")
            if str(idx) == "12":
                freq  = "0" + freq  
            #echo =input("freq3")
                  
            #freq = freq[0:2]+freq[3:8] +" " 
            nLenfreq =len(freq)
            if nLenfreq == 5 :
                freq = freq[0:2]+freq[3:8] +"0 "
            else:
                freq = freq[0:2]+freq[3:6] +" "  #was 3:8
            
            #fCab.write(str(nLenfreq)+"\n")
            #fCab.write("freq: "+freq+"\n")
            #echo=input("freq")
           
     
        if "<mode:"in line or "<MODE:"in line.upper(): 
            #<mode:2>CW
            #echo=input("mode")
            linecase = line.upper()
            idx = linecase.find("MODE")
            numChar = int(line[idx+5])
            mode = line[8:8 + numChar]
            if "SSB" in mode or "LSB" in mode:
                mode = "PH"
                
            #echo=input("mode3")  
            if "FT8" in mode or "FT4" in mode:
                #echo=input("mode2")  
                mode = "DG"
            if "RTTY" in mode:
                #echo=input("mode3")  
                mode = "RY"    
                
            #echo=input("mode")    
            
        if "<qso_date:"in line or "QSO_DATE:" in line.upper():
            #<qso_date:8>20241123
            #            x       
            #            20241123
            #12345678901234567890
            #idx = line.find("qso_date:")
            #echo=input("date")
            date = line[12:20]
            date = date[0:4]+ "-"+ date[4:6]+ "-"+ date[6:8]
    
        if "<call:" in line or "<CALL:" in line.upper():
            
            idx = line.find("<call:")
            #<call:4>CR3A
            #        x      
            #echo=input("call")
            numChar = int(line[6])
            call =line[8:8+numChar]
            # add here 
            nPos =0
            cPrefix =""
            for nPos, char in enumerate(call):
                # enumerate means list and itemize
                # is.digit means is numeric returns bomen -1 or value
            
                nothing = 0
                if char.isdigit():
                    cPrefix =line[8:9+nPos]
                    #echo =input("prefix")
                
            if nPos == -1:
                nothing = 0
                
            if cPrefix == "" :
                echo=print ("numericNotFoundCall = "+ call)
                echo = input ("call error")
                #echo =input("prefix1")

            #add here Prefix
            if cPrefix  in cAccumPrefix:
                nothing =0
            else:
                cAccumPrefix = cAccumPrefix + cPrefix + "    "
                nPrefix  =nPrefix +1
        
            #echo=input("prefix")
        if cShowRST == "Y" :
         
            if "<rst_sent:" in line or "<RST_SENT:" in line.upper():        
                 #<rst_sent:3>-02
                 #012345678901234
                
                 numChar = int(line[10])
                 #echo=input("rsttx2")
                 rsttx = line[12:12+numChar]
                 #echo=input("rsttx")
            
            
            if "<rst_rcvd" in line or "<RST_RCVD" in line.upper():
                 #<rst_rcvd:3>+07
                 #0123456789012345    
                 
                 numChar = int(line[10])
                 rstrx = line[12:12+numChar]   
                 #echo=input("rstrx")
            
            
    
        if "my_cq_zone" in adifCont:  
                # cabrillo rx exchange 
                #<my_cq_zone:1>4
                #0123456789012345
                #echo=input("str")
                if "<my_cq_zone" in line or "<MY_CQ_ZONE" in line.upper():
                    #idx = line.find("my_cq_zone")    #problem for upper case
                    numChar = int(line[12])    #not tested
                    txExch = line[14:15]
                    #echo=input("txExchcq")
                    
        if "county" in adifCont:  
                # cabrillo rx exchange 
                #<cnty:9>TX,Austin
                #01234567890123456
                #echo=input("str")
                if "<cnty" in line or "<CNTY" in line.upper():
                    idx = line.find(">")
                    if idx == 7:
                        numChar = int(line[6])
                        if "3" in adifCont: 
                            rxExch = line[11:14]
                        else: #else 4
                            rxExch = line[11:15]
                            
                    else: # else 8
                        numChar = int(line[6:8])
                        if "3" in adifCont: 
                            rxExch  = line[12:15]
                        else: #else 4
                            rxExch  = line[12:16]
                        
                            
                    #echo=input("rxExchcq")
                    
        if "name" in adifCont:  
                # cabrillo rx exchange 
                #<name:18>TERRY A xxxx
                #01234567890123456
                #echo=input("str")
                if "<name" in line or "<NAME" in line.upper():
                    idx = line.find(">")
                    if idx == 8:
                        numChar = int(line[6])
                        if "5" in adifCont: 
                            rxExch = line[9:14]
                        else: #else 4
                            nothing = 0
                        #    rxExch = line[11:15]
                            
                    else: # else 9
                        nothing = 0
                        #numChar = int(line[6:8])
                        #if "3" in adifCont: 
                        #    rxExch  = line[12:15]
                        #else: #else 4
                        #    rxExch  = line[12:16]
                        
                            
                    #echo=input("rxExchcq")
                     
                    
                    
                    
        
        if "srx_string"in adifCont:
            #echo=input("str")
            if "<srx_string" in line or "<SRX_STRING" in line.upper():  
                # cabrillo rx exchange
                #<srx_string:13>2a wcf    6
                #0123456789012345
                
                #idx = line.find("str_string")
                
    
                #if int(line[13]) == ">":
                if line[13]== ">":
                    numChar = int(line[12])
                    rxExch = line[14:14+numChar]
                else:
                    numChar = int(line[12:14])
                    tempExch = rxExch
                    if numChar >= 18 : 
                        numChar=18 #comment if longer exchange required
                        #echo=input("rxexch truncation at 18")
                    rxExch = line[15:15+numChar]
                    if multstx == "Y":
                        rxExch = tempExch + rxExch
                        
                

                
                #problem here on leng =14
    
        if "cqz" in adifCont :  
            if "cqz"in line or "CQZ" in line.upper():
                # cabrillo tx exchange 
                #<cqz:2>14
                #       x 
                #idx = line.find("cqz")
                #echo=input("stx")
                numChar = int(line[5])
                rxExch = line[7:7+numChar]
                  
        if "stx_string"in adifCont:   
            if "stx_string"in line or "STX_STRING" in line.upper(): 
                # cabrillo tx exchange
                #<stx_string:18>1e tn xxxxxx
                #01234567890123456789012345
                #echo=input("nuch")
                if line[13] ==">":
                    numChar = int(line[12])
                    txExch = line[14:14+numChar]
                    
                else:
                    numChar = int(line[12:14])
                    if numChar >= 18 : 
                        numChar=18 #comment if longer exchange required
                        #echo=input("txexch truncation at 18")
                    
                    txExch = line[15:15+numChar]
                
               
                #echo=input("stx")
            
        if "class" in adifCont:   #1 
            if "<class" in line or "<CLASS" in line.upper():
                
                # cabrillo tx exchange
                #<class:2>1e
                #123456789012345
                numChar = int(line[7])               
                rxExch = line[9:9+numChar]  
                #print (adifCont[11:16] )               
                if "class" in adifCont[11:16] :   
                    rxExc1 = rxExch
                    #echo = input ("r1")
                #greet("class", adifCont, rxExch)  # Calling the procedure
                #echo= input ("class")
                
                #serial stx     srx    
        if "serial" in adifCont: 
            if "<srx:" in line or "<SRX:" in line.upper():           
                #<srx:3>200
                #0123456789012345
                numChar = int(line[5])               
                rxExch = line[7:7+numChar]               
                #echo=input("srx")
    
            if "<stx:" in line or "<STX:" in line.upper():           
                #<stx:3>29
                #0123456789012345
                numChar = int(line[5])
                PadZero = "" 
                if numChar == 2 : 
                    PadZero = "0"
                    numChar = 3
                    txExch =PadZero + line[7:9]         #7 8   
                    
                if numChar == 1 : 
                    PadZero = "00"
                    numChar = 3
                    txExch =PadZero + line[7:8]         #7 8      
                #echo=input("stx")
    
            
        if "SPC1" in adifCont:   
            if "<my_state" in line or "<MY_STATE" in line.upper():
                #<my_state:2>TN
                #123456789012345
                txExch = line[12:14] 
                #echo=input("mystatetx")
        
        if "SPC2" in adifCont:   

            if "<state" in line or "<STATE" in line.upper():  
                #<state:2>FL
                #123456789012345
                tempExch =rxExch
                rxExch = line[9:11]
                #print (adifCont[21:26])
                #echo = input("what")
                if "SPC2 " in adifCont[21:26] : 
                    rxExc2 = rxExch         
                    #echo = input("r2")
                    nothing =0
                    #greet("SPC2", adifCont, rxExch)  # Calling the procedure
                    #echo=input("staterx")

                    
                else :
                    if multstx == "Y":
                        if longExch18== "N":
                            rxExch =tempExch +" "+ rxExch
                        else:
                            tempExch = "{:<8}".format(tempExch)
                            rxExch =tempExch + rxExch
                
        
        
        #always get copy of hisState
        #echo=input ("country =")        
        if "<state" in line or "<STATE" in line.upper(): 
           cFoundState = "Y"       
           #<state:2>FL
           #123456789012345
           #echo=input("<sta")
           if line[10]  ==  "-":
               nothing = 0
               hisState = "nd" 
               #echo=input("nd") 
           
           else:    
               hisState = line[9:11] 
               #echo=input("hisState") 
    
        
        
        #always get copy of his country
        if "<country" in line or "<COUNTRY" in line.upper():
            cFoundCountry = "Y"
            if myCountry in line:
                nothing=0
    
            else: 
                #    <country:10>xxxxxxxxxx
                #    <country:7>Belgium
                #    01234567890123456789012 
                if line[10] ==">" or line[11] ==">":
                    numChar = int(line[9])
                    hisCountry = line[11:11+numChar]
                    #echo=input("hisCountry1") 
                    
                else:
                    numChar = int(line[9:11]) 
                    hisCountry = line[12:12+numChar]
                    #echo=input("hisCountry2") 
                    
        
       
            
                    
        if "arrl_sect" in adifCont:   
             if "arrl_sect" in line or "ARRL_SECT" in line.upper():
                 #<arrl_sect:2>oh
                 #012345678901234567
                 rxExch = line[13:16]
                 #print (adifCont[31:36])
                 #echo = input("what2")
                 if "arrl_" in adifCont[31:36] :  
                     rxExc3 = rxExch
                     #echo = input ("r3")

                 #greet("arrl_sect", rxExc1, rxExc2,rxExc3, adifCont, rxExch)  # Calling the procedure

                 #echo=input("sect")           
    
        if "<name:" in line or "<NAME:" in line.upper():           
            #<name:16>MATTHIAS STRELOW
            cNameFound = "fd"    

    
    
    
          
    if "<eor>"in line or "<EOR>"in line.upper():
        #echo = input ("pause")
        if rxExc1 != "" :
            rxExc1= "{:<3}".format(rxExc1)
            rxExc2= "{:<3}".format(rxExc2)
            rxExc3= "{:<3}".format(rxExc3)
            if rxExc3 != "   " :
                rxExc2 = rxExc3
                rxExc3 = "   "
                
            rxExch = rxExc1 + " " + rxExc2 + " " +  rxExc3 
        rxExc1 = ""
        rxExc2 = ""
        rxExc3 = ""
        txExch = myExchangePrefix+ txExch+ myExchangePostfix
        #echo = input("exchange")
        freq = "{:<5}".format(freq) # was <8
        
        mode = "{:<3}".format(mode)
        mode = mode.upper()
        
        date = "{:<10}".format(date)
        time = "{:<4}".format(time)
        
        myCall = "{:<13}".format(myCall)
        myCall = myCall.upper()
        
        txExch = "{:<6}".format(txExch)
        txExch = txExch.upper()
        
        if longExch18== "Y":
            txExch = "{:<18}".format(txExch)
        txExch = txExch.upper()
        #print (txExch )
        #echo = input ("pause")
        
        call = "{:<13}".format(call)
        call = call.upper()
        
        rxExch = "{:<8}".format(rxExch)
        
  
        rstrx = "{:<3}".format(rstrx)
        rsttx = "{:<3}".format(rsttx)
        
        if longExch18== "Y":
            rxExch = "{:<18}".format(rxExch)
        rxExch = rxExch.upper()
        
        if "//" in rxExch :
            noBustedExchg = noBustedExchg +1
        
        #write line in cabrillo file
        fCab.write("QSO: "+freq +mode+date+" "+time+" "+myCall+" "+rsttx+" "+txExch+" "+call+" "+rstrx +" "+rxExch+" \n")
        #echo = input("fCab write")
        
        # append code added 12/19
        noQSO=noQSO+1
        # define:
        #echo=input("ndom")
        if hisCountry == myCountry or hisCountry == "nd":
            noDom =noDom +1
            #echo=input("ndom")
        
        if hisState in cAccumSt :
            nothing=0
            #echo = input("nothing1")
            
        else:
            if hisCountry != myCountry:
                nothing =0
                #echo=input("nothing2")
            else:
                cAccumSt=cAccumSt+hisState
                noState= noState + 1
                #echo=input("else")
         
        if hisCountry  in cAccumCty:
            nothing=0
            
        else:
           cAccumCty= cAccumCty +hisCountry 
           noContry =noContry +1
           #echo=input("countCTY")
        #dup code continue append

        
        
        
        cQCBsingle =call+"-"+band+ "   "
        if cQCBsingle in cQCBTestlist:
            cQCBDupelist = cQCBDupelist + cQCBsingle 
            noDupe =noDupe+1
            
        else:
            cQCBTestlist =cQCBTestlist+ cQCBsingle 
        # end of append code
        
        #dup code Exchgcontinue append
        cQCBsingle =call+"-"+band+ "-"+rxExch+ "   "
        if cQCBsingle in cQCBDupeExchgTestlist :
            cQCBDupeExchglist = cQCBDupeExchglist + cQCBsingle 
            noDupeExchg =noDupeExchg+1 
            
        else:
            cQCBDupeExchgTestlist  =cQCBDupeExchgTestlist + cQCBsingle 
        # end of append code
       
        cOneExchange = rxExch+ "   "
        if cOneExchange in cTestUniExch:
            cAccumUniExch = cAccumUniExch +  cOneExchange   
            
        else:
            cTestUniExch = cTestUniExch + cOneExchange
            noUniExch =noUniExch +1
        
        if cNameFound == "nd" :           
            cNoNameList =  cNoNameList   + call + "    "
            nNoName = nNoName + 1
        
        
            
        freq = "nd"
        band = "nd"
        mode = "nd"
        date = "nd"
        time = "nd"
        txExch = "//"
        rxExch = "//"
        if multstx == "Y":
           txExch = ""
           rxExch = "" 
        if myExchangePrefix != "" :    
            txExch = ""
            
        call = "nd"
        cNameFound = "nd"
        #rstrx = "599"
        #rsttx = "599"
        
        hisCountry = myCountry
        hisState = "nd"
 
        #echo=input("eor")

#write the footer, close files
fCab.write("END-OF-LOG:\n")

fCab.write("\n")
fCab.write("\n")
fCab.write("\n")
fCab.write("\n")
fCab.write("X MYCONVPY.PY SUMMARY: \n")
fCab.write("\n")
fCab.write("X contest filter:"+ cContest + "\n")


fCab.write("X noQSO=         " +str(noQSO)+"  \n")
if cHorizontalFormat == "N":
    if cFoundCountry == "Y":
        fCab.write("X noDomes=       " +str(noDom)+" \n")
    
    if cFoundState == "Y":
        fCab.write("X noState=       " +str(noState)+"(always domestic)  \n")
    
    if cFoundCountry == "Y":
        fCab.write("X noDXCC/WAE=    " +str(noContry)+"  \n")
    
    fCab.write("\n")
    fCab.write("X noDupe=        " +str(noDupe)+"  \n")
    fCab.write("X Dupes:        " +cQCBDupelist +"  \n")
    
    fCab.write("\n")
    fCab.write("X noDupeExch=    " +str(noDupeExchg)+"  \n")
    fCab.write("X DupesExch:    " +cQCBDupeExchglist +"  \n")
    
    fCab.write("\n")
    fCab.write("X noUniExch =    " +str(noUniExch)+"  \n")
    
    fCab.write("\n")
    if noB160 > 0 : fCab.write("X noBand160 =    " +str(noB160)+"  \n")
    if noB80 > 0 : fCab.write("X noBand80 =     " +str(noB80)+"  \n")
    if noB40 > 0 : fCab.write("X noBand40 =     " +str(noB40)+"  \n")
    if noB20 > 0 : fCab.write("X noBand20 =     " +str(noB20)+"  \n")
    if noB15 > 0 : fCab.write("X noBand15 =     " +str(noB15)+"  \n")
    if noB10 > 0 : fCab.write("X noBand10 =     " +str(noB10)+"  \n")
    if noB6 > 0 : fCab.write("X noBand6 =      " +str(noB6)+"  \n")
    if noB2 > 0 : fCab.write("X noBand2 =      " +str(noB2)+"  \n")
    
    fCab.write("\n")
    fCab.write("X nPrefix=        " +str(nPrefix) +"  \n")
    fCab.write("X Prefixs:        " +cAccumPrefix +"  \n")

    
    
    fCab.write("\n")
    fCab.write("X possible callsignBusted=  "+ cNoNameList + "  \n")
    
    fCab.write("\n")
    noLikeError = noBustedExchg +noDupe +noLikeError+ nNoName
        #can produce > 1 errors per qso
    fCab.write("X likely Errors=  "+ str(noLikeError) + "  \n")
    
    if noQSO >= 0 :
        fCab.write("\n")
        
        noErrorRate= 100* noLikeError/ noQSO
        reErrorRate = str(noErrorRate)
        reErrorRate= reErrorRate[0:4]
        fCab.write("X errorRate=      "+ reErrorRate+ "  \n")
    
    fCab.write("\n")
    fCab.write('X adif fields: adifCont= "'+ adifCont + '"  \n')
    
    fCab.write("\n")
    fCab.write('X myExchangePrefix= "'+ myExchangePrefix + '"  \n')
    fCab.write("\n")
    fCab.write('X myExchangePostfix = "'+ myExchangePostfix + '"  \n')


    

fCab.close()
fAdif.close()
echo = print ("ended at EOJ")
#dingsound.ding()

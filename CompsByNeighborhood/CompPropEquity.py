import sys
import requests 
import pdb      #tracing
import datetime
import time
from bs4 import BeautifulSoup

startTime                       = datetime.datetime.now()
completionTime                  = ''

pinToUse                        = ''
goodPIN                         = True
pin_counter                     = 0
recordsWrittenToFile_counter    = 0
pinsInError_counter             = 0
internetConnectionError_counter = 0
internetConnectionError         = 0
waitForConnectionTimer          = 5 #seconds

pinSourceFile                   = '../TestData/1000TestPins.txt'        # 25TestPins.txt or 1000TestPins.txt
dataToWriteFile                 = 'CompPropEquity_Data.txt'
errorFile                       = 'CompPropEquity_Error.txt'

dataFileToWrite                 = open(dataToWriteFile, 'w')
errorFileToWrite                = open(errorFile, 'w')
#url                            = defined lower in the code so that pinToUse gets evaluated properly 

print("Working from file: " + pinSourceFile)
with open(pinSourceFile, 'r') as f:
    for line in f:
        if (line.strip() == ""):
            continue
        #print(line)
        pin_counter += 1

        equity_comp_dictionary = {  'subject_pin':'#',
                                    'distance':'#',
                                    'comp_pin':'#',
                                    'tax_payers_street_address':'EQUITY'}
        
        pinToUse = line.strip()[:10] # some pins have more than 10 digits but the extra digits are not needed for the search

        for x in range(0,10):
            try:
                #print("")
                #print("------------- start URL grab ---------------")
                #print("https://apps03.lakecountyil.gov/comparables/PTAIPicker.aspx?PIN="+ pinToUse + "&TYPE=A&POPUP=Y")
                startURLRequest = datetime.datetime.now()

                html_contents = requests.get('https://apps03.lakecountyil.gov/comparables/PTAIPicker.aspx?PIN='+ pinToUse + '&TYPE=A&POPUP=Y', timeout=3).text 
                html_soup = BeautifulSoup(html_contents, 'html.parser')
                
                #print("Duration of transaction: " + str((round((datetime.datetime.now() - startURLRequest).total_seconds()))))
                #print("------------- End of URL grab ---------------")
                #print("")
                internetConnectionError = 0
                break
            except (requests.exceptions.RequestException):
                print("Internet connectivity or latency issues... Sleep for 5 seconds and try again")
                internetConnectionError +=1
                if internetConnectionError <= 1:
                    errorFileToWrite.write("New Connection Error :" + 'https://apps03.lakecountyil.gov/comparables/PTAIPicker.aspx?PIN='+ pinToUse + '&TYPE=A&POPUP=Y\r')
                    internetConnectionError_counter +=1
                time.sleep(waitForConnectionTimer)
            finally:
                if internetConnectionError == 9:
                    sys.exit("Internet Connection is not sufficient to keep going.... ending program at time: " + str(datetime.datetime.now()))



        # --------------------------------
        # Extract Subject Pin from Page
        # --------------------------------
        for table in html_soup.find_all('table', id='tblPicker'):
            goodPIN = True #assumed good until it fails the tests below

            #-----------------------------------------------------------
            # Check for either Invalid PIN or No Comparable Properties
            #-----------------------------------------------------------
            for table.rows in table.find('thead').find_all('th',{'id':'Th7'}):
                for value in table.rows.find('',{'id':'lblvaluetype'}):
                    if (value == '(Assessed Value)'):
                        errorFileToWrite.write("Invalid Pin :\t" + line)
                        pinsInError_counter += 1
                        goodPIN = False
                        continue

            for compTable in html_soup.find_all('table', id='tblComp', limit=1):
                if (compTable.text.strip() == 'No Properties Match Criteria'):
                    errorFileToWrite.write("No Properties Match Criteria for :" + line)
                    pinsInError_counter += 1
                    goodPIN = False
                    continue
                else:
                    equity_comp_dictionary['subject_pin'] = table.find('',{'id':'lblPIN2'}).text
            #-------------------------------------------------------------------------------------

                # -----------------------------------
                # Extract data elements from the page
                # -----------------------------------
                if (goodPIN):

                    for compTable in html_soup.find_all('table', {'id':'tblComp'}, limit=1):    # Still in the same tableComp structure    
                        for rows in compTable.find('tbody').find_all('tr'):

                            for pin in rows.find_all('',{'target':'_blank'}):  
                                if (pin.text != ''):
                                    equity_comp_dictionary['comp_pin'] = pin.text
                                    break

                            for distance in rows.find_all('',{'align':'right'}):  
                                if (distance.text != '' and distance.text != '0'):
                                    equity_comp_dictionary['distance'] = distance.text
                        
                            # -----------------------------------------------------
                            # only write the record if it's a valid PIN with Comps
                            # -----------------------------------------------------
                            if ((equity_comp_dictionary['comp_pin']) == '#'):
                                continue
                            else: 
                                record = ''
                                for key,val in equity_comp_dictionary.items():
                                    record += val + '|'
                                record += '\r'
                                dataFileToWrite.write(record)
                                recordsWrittenToFile_counter += 1

                   # print(allData)
                    #print('******************** End of allData set **********************************')

dataFileToWrite.close
#---------------------------------------------
# Show statistics of the program execution
#---------------------------------------------
completionTime = datetime.datetime.now()
print('#-------------------------------------------------------------------')
print('#                        Program Statistics                         ')
print('#-------------------------------------------------------------------')
print("Program execution time in Seconds:   "       + str((completionTime - startTime).total_seconds()) + '\tRecords/Second\t: ' + str((round(((completionTime - startTime).total_seconds()/pin_counter),2))))
print("Records read from File:              "       + pinSourceFile + '\t\t: ' + str(pin_counter))
print("Records written to Data File:        "       + dataToWriteFile + '\t: ' + str(recordsWrittenToFile_counter))
print("Records written to Error File:       "       + errorFile + '\t: ' + str(pinsInError_counter) + '\r')
print("\t\t\t\t     Internet Connection Errors "    + ": " + str(internetConnectionError_counter))




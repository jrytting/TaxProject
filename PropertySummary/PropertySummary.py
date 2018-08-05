import requests 
import pdb      #tracing
import datetime
from bs4 import BeautifulSoup
import math
import time
import sys


startTime                       = datetime.datetime.now()
completionTime                  = ''

pinCounter                      = 0
pinToUse                        = ''
invalidPin                      = "Invalid PIN"
goodPIN                         = True
record_counter                  = 0
recordsWrittenToFile_counter    = 0
pinsInError_counter             = 0
saleDataWrite_counter           = 0
internetConnectionError_counter = 0
internetConnectionError         = 0
waitForConnectionTimer          = 5 #seconds
pinDataSet                      = []

pinSourceFile                   = '../TestData/1000TestPins.txt'        # 25TestPins.txt or 1000TestPins.txt
dataToWriteFile                 = 'PropertySummary_Data.txt'
errorFile                       = 'PropertySummary_Error.txt'
saleHistoryFile                 = 'PropertySalesHistory.txt'

dataFileToWrite                 = open(dataToWriteFile, 'w')
errorFileToWrite                = open(errorFile, 'w')
saleHistoryToWrite              = open(saleHistoryFile, 'w')
#url                            = defined lower down in the code so that pinToUse gets evaluated properly

permanent_index_number_labels   = {'PropertyCharacteristics1_lblPin'}
city_labels                     = {'PropertyCharacteristics1_lblCity'}
zipcode_labels                  = {'PropertyCharacteristics1_lblZipCode'}
township_labels                 = {'PropertyCharacteristics1_lblTownship'}
assessment_date_labels          = {'PropertyCharacteristics1_lblAssessmentDate'}
property_class_labels           = {'PropertyCharacteristics1_lblPropertyClass'}
class_description_labels        = {'PropertyCharacteristics1_lblClassDescription'}
multiple_buildings_labels       = {'PropertyCharacteristics1_lblMultipleBuildings'}

print("Working from file: " + pinSourceFile)
print(datetime.datetime.now())

with open(pinSourceFile, 'r') as f:
    for line in f:
        if (line == ""): 
            continue
        record_counter += 1
        pinToUse = line.replace('\n', '')[:10]

        #print (pinToUse)
        #subjectpin, compPin1, compPin2, compPin3 = '0302300025','0302300026','0302300027','0302300028'  
        #pdb.set_trace()

        for x in range(0,10):
            try:
                #print("")
                #print("------------- start URL grab ---------------")
                #print('http://apps01.lakecountyil.gov/spassessor/comparables/PTAIpin.aspx?PIN=' + pinToUse)
                startURLRequest = datetime.datetime.now()
                html_contents = requests.get('http://apps01.lakecountyil.gov/spassessor/comparables/PTAIpin.aspx?PIN=' + pinToUse, timeout=3).text 
                html_soup = BeautifulSoup(html_contents, 'html.parser')
                #print("Duration of transaction: " + str((round((datetime.datetime.now() - startURLRequest).total_seconds()))))
                #print("------------- End of URL grab ---------------")
                #print("")
                internetConnectionError = 0
                break
            except (requests.exceptions.RequestException):
                print("Something is wrong here... Sleep for 5 seconds and try again")
                internetConnectionError +=1
                if internetConnectionError <= 1:
                    errorFileToWrite.write("New Connection Error :" + 'http://apps01.lakecountyil.gov/spassessor/comparables/PTAIpin.aspx?PIN=' + pinToUse + '\r')
                    internetConnectionError_counter +=1
                time.sleep(waitForConnectionTimer)
            finally:
                if internetConnectionError == 9:
                    sys.exit("Internet Connection is not sufficient to keep going.... ending program at time: " + str(datetime.datetime.now()))

        
        for table in html_soup.find_all('table', id='PropertyCharacteristics1_tblPropertyAddress'):
            try:
                #todo - Check for invalid pin

                #Get PIN
                dataFields = table.find(id=permanent_index_number_labels)
                subjectpin = str(dataFields.text).replace('-','').strip()[:10]
                if (subjectpin == ''):
                    raise exception()

                #Get City
                dataFields = table.find(id=city_labels)
                city = str(dataFields.text).replace('-','').strip()

                #Get Zipcode
                dataFields = table.find(id=zipcode_labels)
                zipcode = str(dataFields.text).replace('-','').strip()[:5]

                #Get Township
                dataFields = table.find(id=township_labels)
                township = str(dataFields.text).replace('-','').strip()

                #Get Assessment Date
                dataFields = table.find(id=assessment_date_labels)
                assessmentDate = str(dataFields.text).replace('-','').strip()

                for table in html_soup.find_all('table', id='PropertyCharacteristics1_tblPropertyCharacteristics'):
                    #Get Property Class
                    dataFields = table.find(id=property_class_labels)
                    propertyClass = str(dataFields.text).replace('-','').strip()

                    #Get Class Description
                    dataFields = table.find(id=class_description_labels)
                    classDescription = str(dataFields.text).replace('-','').strip()

                    #Get Multiple Buildings
                    dataFields = table.find(id=multiple_buildings_labels)
                    multipleBuildings = str(dataFields.text).replace('-','').strip()
           
            except KeyboardInterrupt:
                print('You cancelled the operation.')
                
            except:
                #print("Something when wrong skipping PIN... but don't stop the program: PIN:  " + subjectpin + "\r")         
                errorFileToWrite.write("Invalid PIN:  " + pinToUse + "\r")
                pinsInError_counter += 1

        if (subjectpin != ''):
            record = subjectpin + "|" + city + "|" + zipcode + '|' + township + "|" + assessmentDate + "|" + propertyClass + "|" + classDescription + "|" + multipleBuildings + "\r"
            dataFileToWrite.write(record)
            recordsWrittenToFile_counter +=1



        for table in html_soup.find_all('table', id='PropertyCharacteristics1_tblPropertySalesHistory'):
            #Get Sales History/Summary Informatoin if it exists 
            #tables = table.find(style="text-align:center;color:#FF0000;font-family:Arial, Helvetica, sans-serif;")
            #if tables is not None:
            #salesSummary = str(dataFields.text).replace('-','').strip()
            for rows in table.find_all('tr', style="text-align:center;font-size:small;font-family:Arial, Helvetica, sans-serif;"):
                dataToSplit = ''
                for dataFields in rows.find_all('td'):
                    dataToSplit += (dataFields.text).replace(',','').replace('$','').replace('/','-') + ","

                dateOfSale, saleAmount, salesValidation, compulsarySale = str(dataToSplit[:-1]).split(',')
                saleHistoryToWrite.write(pinToUse + "|" + dateOfSale + "|" +saleAmount + "|" + salesValidation + "|" + compulsarySale +'\r')
                saleDataWrite_counter +=1





#---------------------------------------------
# Show statistics of the program execution
#---------------------------------------------
completionTime = datetime.datetime.now()
print('#-------------------------------------------------------------------')
print('#                        Program Statistics                         ')
print('#-------------------------------------------------------------------')
print("Program execution time in Seconds: " + str((completionTime - startTime).total_seconds()) + '\tRecords/Second:   ' + str((round(((completionTime - startTime).total_seconds()/record_counter),2))))
print("Program wrote the folliwing lines: " + "\t\t" + str(record_counter))
print("Records read from File:            " + pinSourceFile + '\t\t: ' + str(record_counter))
print("Records written to Data File:      " + dataToWriteFile + '\t: ' + str(recordsWrittenToFile_counter))
print("Sales Records written to Data File:" + saleHistoryFile + '\t: ' + str(saleDataWrite_counter))
print("Records written to Error File:     " + errorFile + '\t: ' + str(pinsInError_counter))
print("\t\t\t\t     Internet Connection Errors "    + ": " + str(internetConnectionError_counter))
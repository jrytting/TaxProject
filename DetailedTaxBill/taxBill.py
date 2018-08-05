import requests  #
import pdb  # tracing
import datetime
from bs4 import BeautifulSoup
import json
import time
import sys

startTime                       = datetime.datetime.now()
completionTime                  = ''

pinToUse                        = ''
skipIt                          = False
record_counter                  = 0
recordsWrittenToFile_counter    = 0
pinsInError_counter             = 0
internetConnectionError_counter = 0
internetConnectionError         = 0
waitForConnectionTimer          = 5 #seconds

pinSourceFile                   = '../TestData/1000TestPins.txt'        # 25TestPins.txt or 1000TestPins.txt
dataToWriteFile                 = 'TaxBill_Data.txt'
errorFile                       = 'TaxBillData_Error.txt'

dataFileToWrite                 = open(dataToWriteFile, 'w')
errorFileToWrite                = open(errorFile, 'w')

tax_bill_dictionary = {'pin': '#',
                       'tax_year': '#',
                       'tax_payers_name': '#',
                       'tax_payers_street_address': '#',
                       'tax_payers_city': '#',
                       'tax_payers_state': '#',
                       'tax_payers_zipcode': '#',
                       'legal_description1': '#',
                       'legal_description2': '#',
                       'land_value': '#',
                       'building_value': '#',
                       'state_multiplier': '#',
                       'equalized_value': '#',
                       'farm_land_and_bldg_value': '#',
                       'state_assessed_pollution_ctrl': '#',
                       'state_assessed_railroads': '#',
                       'total_assessed_value': '#',
                       'fully_exempt': '#',
                       'senior_freeze': '#',
                       'home_improvement': '#',
                       'limited_homestead': '#',
                       'senior_homestead': '#',
                       'veterans_disabled': '#',
                       'returning_veteran': '#',
                       'taxable_valuations': '#',
                       'tax_rate': '#',
                       'real_estate_tax': '#',
                       'special_assessment': '#',
                       'drainage': '#',
                       'total_current_year_tax': '#',
                       'omitted_tax': '#',
                       'forfeited_tax': '#',
                       'total_tax_billed': '#',
                       'interest_due_as_of_date': '#',
                       'interest_due': '#',
                       'cost': '#',
                       'amount_billed': '#',
                       'fair_market_value': '#',
                       'special_notes1': '#',
                       'special_notes2': '#',
                       'special_notes3': '#',
                       'special_notes4': '#',
                       'special_notes5': '#',
                       'special_notes6': '#',
                       'special_notes7': '#',
                       'first_installment_due': '#',
                       'first_installment_amt': '#',
                       'second_installment_due': '#',
                       'second_installment_amt': '#'}

print("Working from file: " + pinSourceFile)
print(datetime.datetime.now())
# print(json.dumps(tax_bill_dictionary, indent=4, sort_keys=False))


with open(pinSourceFile, 'r') as f:
    for line in f:
        record_counter +=1
        # print(line)
        # pdb.set_trace()
        z = line.strip()
        #z="0301300047"  #ToDo Hardcoded Value for Testing only
        pinToUse = '-'.join([z[:2], z[2:4], z[4:7], z[7:10]])

        url = 'https://apps03.lakecountyil.gov/treasurer/collbook/collbook4.asp?PIN=' + pinToUse + '&unit=0000'

        for x in range(0,10):
            try:
                #print("")
                #print("------------- start URL grab ---------------")
                #print('https://apps03.lakecountyil.gov/comparables/PTAIPicker.aspx?PIN='+pinToUse+'&TYPE=S&POPUP=Y')
                startURLRequest = datetime.datetime.now()
                r = requests.get(url, timeout=10)
                html_contents = r.text
                # print(html_contents)
                html_soup = BeautifulSoup(html_contents, 'html.parser')
                #print("Duration of transaction: " + str((round((datetime.datetime.now() - startURLRequest).total_seconds()))))
                #print("------------- End of URL grab ---------------")
                #print("")
                internetConnectionError = 0
                break
            except requests.exceptions.RequestException as e:
                print(e)
                print("Sleep for 5 seconds and try again")
                internetConnectionError +=1
                if internetConnectionError <= 1:
                    errorFileToWrite.write("New Connection Error :" + 'https://apps03.lakecountyil.gov/comparables/PTAIPicker.aspx?PIN='+ pinToUse + '&TYPE=A&POPUP=Y\r')
                    internetConnectionError_counter +=1
                time.sleep(waitForConnectionTimer)
            finally:
                if internetConnectionError == 9:
                    sys.exit("Internet Connection is not sufficient to keep going.... ending program at time: " + str(datetime.datetime.now()))


        pageTables = html_soup.find_all('table')
        for tables in pageTables:
            for rows in tables.find_all('tr', '', limit=1):
                for msg in rows.find_all('', {'class': 'msg'}, limit=1):
                    if msg.text == 'Pin is missing or incorrect.':
                        errorFileToWrite.write("PIN: " + pinToUse + ", Error Msg: " + msg.text + ", URL: " + url + '\r')
                        pinsInError_counter +=1
                        skipIt = True
            if (skipIt):
                skipIt = False  # reset value
                break
            else:
                pass

        # We know know we have a valid PIN
        tax_bill_dictionary['pin'] = pinToUse.replace('-', '')  # strip out the dashes
        # pdb.set_trace()
        # --------------------------------------------------------------------------------------
        # Scrape the following fields:
        #   tax_payers_name
        #   tax_Payers_street_address
        #   tax_payers_city
        #   tax_payers_zipcode

        def tax_payer(taxpayer):
            tax_bill_dictionary['tax_payers_name'] = taxpayer;

        def tax_payers_street_address(address):
            tax_bill_dictionary['tax_payers_street_address'] = address;

        def tax_payers_city_st_zip(citystzip):
            city, state = citystzip.split(',')
            state, zipcode = state.split()

            tax_bill_dictionary['tax_payers_city'] = city
            tax_bill_dictionary['tax_payers_state'] = state
            tax_bill_dictionary['tax_payers_zipcode'] = zipcode

        options = {1 : tax_payer,
                   2 : tax_payers_street_address,
                   3 : tax_payers_city_st_zip,}

        for table1 in html_soup.find_all('table', id='table1',limit=1):
            counter = 1
            for table1.rows in table1.find_all('p', {'class':'blockindent1', 'style':'margin-top: 0; margin-bottom: 0'}):
                options[counter]((table1.rows.text).strip("\r\t\n\u00a0"))
                counter +=1

        # --------------------------------------------------------------------------------------

        data = []
        for table5 in html_soup.find_all('table', id='table5', limit=1):
            counter = 0;
            for table5.rows in table5.find_all('td', {'width':'102'}):
                if ((table5.rows.text).strip() == 'Tax Year'):
                    continue
                else:
                    tax_bill_dictionary['tax_year'] = (table5.rows.text).strip()
                    dummy1,tax_rate,dummy2 = str(table5.rows.find_next_siblings()).split(', ')
                    tax_bill_dictionary['tax_rate'] = BeautifulSoup(tax_rate, 'html.parser').text
                    #print(json.dumps(tax_bill_dictionary, indent=4, sort_keys=False))
                    break

            #pdb.set_trace()
            rowCount = 0
            for table5.rows in table5.find_all('tr',recursive=False):
                rowCount +=1
                #if (rowCount == 7):
                    #pdb.set_trace()
                #print('Row Counter is: ' + str(rowCount))
                dataCount = 0
                for table5.data in table5.rows.find_all('td', recursive=False):
                    dataCount +=1

                    if(table5.data.text == "Legal Description:"):
                        #pdb.set_trace()
                        legalDescription = ((table5.data.find_next_siblings())[0].text)[:198]
                        tax_bill_dictionary['legal_description1'] = (legalDescription[:99]).strip('\r\n\t\t')                              #((legalDescription[0].text).strip('\r\n\t\t'))[:99]
                        tax_bill_dictionary['legal_description2'] = legalDescription[99:].strip('\r\n\t\t')
                        continue

                    elif(table5.data.text == "Land Value"):
                        landValue = table5.data.find_next_siblings()
                        tax_bill_dictionary['land_value'] = landValue[1].text 
                        continue  
                        
                    elif (table5.data.text == "+ Building Value"):
                        buldingValue = table5.data.find_next_siblings()
                        tax_bill_dictionary['building_value'] = buldingValue[1].text
                        continue

                    elif (table5.data.text == "x State Multiplier"):
                        stateMultiplier = table5.data.find_next_siblings()
                        tax_bill_dictionary['state_multiplier'] = stateMultiplier[1].text
                        continue
                    
                    elif (table5.data.text == "= Equalized Value"):
                        equalizer = table5.data.find_next_siblings()
                        tax_bill_dictionary['equalized_value'] = equalizer[1].text
                        continue

                    elif (table5.data.text == "+ Farm Land and Bldg Value"):
                        farmandbldgValue = table5.data.find_next_siblings()
                        tax_bill_dictionary['farm_land_and_bldg_value'] = farmandbldgValue[1].text
                        continue

                    elif (table5.data.text == "+ State Assessed Pollution Ctrl."):
                        pollutionCtrl = table5.data.find_next_siblings()
                        tax_bill_dictionary['state_assessed_pollution_ctrl'] = pollutionCtrl[1].text
                        continue

                    elif (table5.data.text == "+ State Assessed Railroads"):
                        railroads = table5.data.find_next_siblings()
                        tax_bill_dictionary['state_assessed_railroads'] = railroads[1].text
                        continue

                    elif (table5.data.text == "= Total Assessed Value"):
                        assessedValue = table5.data.find_next_siblings()
                        tax_bill_dictionary['total_assessed_value'] = assessedValue[1].text
                        continue

                    elif (table5.data.text == "- Fully Exempt"):
                        fullyExempt = table5.data.find_next_siblings()
                        tax_bill_dictionary['fully_exempt'] = fullyExempt[1].text
                        continue

                    elif (table5.data.text == "- Senior Freeze"):
                        seniorFreeze = table5.data.find_next_siblings()
                        tax_bill_dictionary['senior_freeze'] = seniorFreeze[1].text
                        continue

                    elif (table5.data.text == "- Home Improvement"):
                        homeImprovement = table5.data.find_next_siblings()
                        tax_bill_dictionary['home_improvement'] = homeImprovement[1].text
                        continue

                    elif (table5.data.text == "- General Homestead"):
                        generalHomestead = table5.data.find_next_siblings()
                        tax_bill_dictionary['limited_homestead'] = generalHomestead[1].text
                        continue

                    elif (table5.data.text == "- Senior Homestead"):
                        seniorHomestead = table5.data.find_next_siblings()
                        tax_bill_dictionary['senior_homestead'] = seniorHomestead[1].text
                        continue

                    elif (table5.data.text == "- Veterans/Disabled"):
                        veterans = table5.data.find_next_siblings()
                        tax_bill_dictionary['veterans_disabled'] = veterans[1].text
                        continue

                    elif (table5.data.text == "- Returning Veteran"):
                        veteransReturn = table5.data.find_next_siblings()
                        tax_bill_dictionary['returning_veteran'] = veteransReturn[1].text
                        continue

                    elif (table5.data.text == "= Taxable Valuation"):
                        taxableValuation = table5.data.find_next_siblings()
                        tax_bill_dictionary['taxable_valuations'] = taxableValuation[1].text
                        continue

                    elif (table5.data.text == "x Tax Rate"):
                        taxRate = table5.data.find_next_siblings()
                        tax_bill_dictionary['tax_rate'] = taxRate[1].text
                        continue

                    elif (table5.data.text == "= Real Estate Tax"):
                        realEstateTax = table5.data.find_next_siblings()
                        tax_bill_dictionary['real_estate_tax'] = realEstateTax[1].text
                        continue

                    elif (table5.data.text == "+ Special Service Area"):
                        specialServicesArea = table5.data.find_next_siblings()
                        tax_bill_dictionary['special_assessment'] = specialServicesArea[1].text
                        continue

                    elif (table5.data.text == "+ Drainage"):
                        drainage = table5.data.find_next_siblings()
                        tax_bill_dictionary['drainage'] = drainage[1].text
                        continue

                    elif (table5.data.text == "= Total Current Year Tax"):
                        totalCurrentYearTax = table5.data.find_next_siblings()
                        tax_bill_dictionary['total_current_year_tax'] = totalCurrentYearTax[1].text
                        continue

                    elif (table5.data.text == "+ Omitted Tax"):
                        omittedTax = table5.data.find_next_siblings()
                        tax_bill_dictionary['omitted_tax'] = omittedTax[1].text
                        continue

                    elif (table5.data.text == "+ Forfeited Tax"):
                        forfeitedTax = table5.data.find_next_siblings()
                        tax_bill_dictionary['forfeited_tax'] = forfeitedTax[1].text
                        continue

                    elif (table5.data.text == "= Total Tax Billed"):
                        totalTaxBilled = table5.data.find_next_siblings()
                        tax_bill_dictionary['total_tax_billed'] = totalTaxBilled[1].text
                        continue

                    
                    elif (table5.data.text == "+ Interest Due as of"):
                        interestDue = table5.data.find_next_siblings()
                        interestDate,interestAmt = str(table5.data.find_next_siblings()).split(', ')
                        tax_bill_dictionary['interest_due_as_of_date'] = BeautifulSoup(interestDate, 'html.parser').text.replace('/','-')
                        tax_bill_dictionary['interest_due'] = BeautifulSoup(interestAmt, 'html.parser').text
                        continue

                    elif (table5.data.text == "+ Cost"):
                        cost = table5.data.find_next_siblings()
                        tax_bill_dictionary['cost'] = cost[1].text
                        continue

                    elif (table5.data.text == "= AMOUNT BILLED"):
                        amountBilled = table5.data.find_next_siblings()
                        tax_bill_dictionary['amount_billed'] = amountBilled[1].text
                        continue

                    elif (table5.data.text == "Fair Market Value"):
                        fairMarketValue = table5.data.find_next_siblings()
                        tax_bill_dictionary['fair_market_value'] = fairMarketValue[1].text
                        continue

                    elif (table5.data.text == "1st Installment Due"):
                        firstInstallDue = table5.data.find_next_siblings()
                        firstDate,firstAmt = str(table5.data.find_next_siblings()).split(', ')
                        tax_bill_dictionary['first_installment_due'] = BeautifulSoup(firstDate, 'html.parser').text.replace('/','-')
                        tax_bill_dictionary['first_installment_amt'] = BeautifulSoup(firstAmt, 'html.parser').text
                        continue

                    
                    elif (table5.data.text == "2nd Installment Due"):
                        secondInstallDue = table5.data.find_next_siblings()
                        secondDate,secondAmt = str(table5.data.find_next_siblings()).split(', ')
                        tax_bill_dictionary['second_installment_due'] = BeautifulSoup(secondDate, 'html.parser').text.replace('/','-')
                        tax_bill_dictionary['second_installment_amt'] = BeautifulSoup(secondAmt, 'html.parser').text


                    #print(json.dumps(tax_bill_dictionary, indent=4, sort_keys=False))



        # scrub the data in the dictionary to remove characters the DB won't like
        for key,val in tax_bill_dictionary.items():
            if (val.strip().replace(u"\u00A0", "") == ""):
                val = '0'

            if ((key == 'interest_due_as_of_date' or key == 'first_installment_due' or key == 'second_installment_due')) and (val == '0'):
                val = '0000-00-00'

            tax_bill_dictionary[key] = val.strip(',$[]').replace(u"\u00A0", "").replace(',',"").replace("&nbsp", " ")

        record = ''
        for key,val in tax_bill_dictionary.items():
            record += val + '|'
        record += '\r'
        dataFileToWrite.write(record)
        recordsWrittenToFile_counter += 1
    


print(datetime.datetime.now())

#---------------------------------------------
# Show statistics of the program execution
#---------------------------------------------
completionTime = datetime.datetime.now()
print('#-------------------------------------------------------------------')
print('#                        Program Statistics                         ')
print('#-------------------------------------------------------------------')
print("Program execution time in Seconds: " + str((completionTime - startTime).total_seconds()) + '\tRecords/Second:   ' + str((round(((completionTime - startTime).total_seconds()/record_counter),2))))
print("Records read from File:            " + pinSourceFile + '\t\t: ' + str(record_counter))
print("Records written to Data File:      " + dataToWriteFile + '\t\t: ' + str(recordsWrittenToFile_counter) + '\r')
print("Records written to Error File:     " + errorFile + '\t: ' + str(pinsInError_counter))
print("\t\t\t\t     Internet Connection Errors "    + ": " + str(internetConnectionError_counter))

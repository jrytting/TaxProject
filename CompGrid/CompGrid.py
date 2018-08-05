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
internetConnectionError_counter = 0
internetConnectionError         = 0
waitForConnectionTimer          = 5 #seconds
pinDataSet                      = []

pinSourceFile                   = '../TestData/1000TestPins.txt'        # 25TestPins.txt or 1000TestPins.txt
dataToWriteFile                 = 'CompGrid_Data.txt'
errorFile                       = 'CompGrid_Error.txt'

dataFileToWrite                 = open(dataToWriteFile, 'w')
errorFileToWrite                = open(errorFile, 'w')
#url                            = defined lower down in the code so that pinToUse gets evaluated properly

permanent_index_number_labels                                       = {'lblSPin','lblCPin1','lblCPin2','lblCPin3'}
street_address_labels                                               = {'lblSAddress','lblCAddress1','lblCAddress2','lblCAddress3'}
neighborhood_number_labels                                          = {'lblSNeighborhood','lblCNeighborhood1','lblCNeighborhood2','lblCNeighborhood3'}
neighborhood_name_labels                                            = {'lblSNeighDesc','lblCNeighDesc1','lblCNeighDesc2','lblCNeighDesc3'}
land_size_labels                                                    = {'lblSAmtLand','lblCAmtLand1','lblCAmtLand2','lblCAmtLand3'}
house_type_code_labels                                              = {'lblSHTC','lblCHTC1','lblCHTC2','lblCHTC3'}
structure_type_stories_labels                                       = {'lblSStories','lblCStories1','lblCStories2','lblCStories3'}
exterior_cover_labels                                               = {'lblSConstruct','lblCConstruct1','lblCConstruct2','lblCConstruct3'}
quality_grade_labels                                                = {'lblSQuality','lblCQuality1','lblCQuality2','lblCQuality3'}
condition_labels                                                    = {'lblSCondition','lblCCondition1','lblCCondition2','lblCCondition3'}
year_built_labels                                                   = {'lblSYearBuilt','lblCYearBuilt1','lblCYearBuilt2','lblCYearBuilt3'}
effective_age_labels                                                = {'lblSEffYear','lblCEffYear1','lblCEffYear2','lblCEffYear3'}
land_assessed_value_labels                                          = {'lblSLandAmt','lblCLandAmt1','lblCLandAmt2','lblCLandAmt3'}
building_assessed_value_labels                                      = {'lblSAmtImp','lblCAmtImp1','lblCAmtImp2','lblCAmtImp3'}
total_assessed_value_labels                                         = {'lblSAmtTotal','lblCAmtTotal1','lblCAmtTotal2','lblCAmtTotal3'}
land_market_value_labels                                            = {'lblSLandMV','lblCLandMV1','lblCLandMV2','lblCLandMV3'}
building_market_value_labels                                        = {'lblSBldgMV','lblCBldgMV1','lblCBldgMV2','lblCBldgMV3'}
total_market_value_labels                                           = {'lblSTMV','lblCTMV1','lblCTMV2','lblCTMV3'}
primary_land_method_labels                                          = {'lblSLandMethod','lblCLandMethod1','lblCLandMethod2','lblCLandMethod3'}
land_price_per_size_assessed_value_labels                           = {'lblSLandSqFtAV','lblCLandSqFtAV1','lblCLandSqFtAV2','lblCLandSqFtAV3'}
building_price_per_agla_assessed_value_labels                       = {'lblSBldgSqFtAV','lblCBldgSqFtAV1','lblCBldgSqFtAV2','lblCBldgSqFtAV3'}
total_value_per_agla_market_value_labels                            = {'lblSTotalSqFtMV','lblCTotalSqFtMV1','lblCTotalSqFtMV2','lblCTotalSqFtMV3'}
last_sale_amount_labels                                             = {'lblSSale1Price','lblCSale1Price1','lblCSale1Price2','lblCSale1Price3'}
date_of_sale_labels                                                 = {'lblSSale1Date','lblCSale1Date1','lblCSale1Date2','lblCSale1Date3'}
sales_validation_labels                                             = {'lblSQualSale1Text','lblCQualSale1Text1','lblCQualSale1Text2','lblCQualSale1Text3'}
compulsory_sale_labels                                              = {'lblSTranstype1Text','lblCTranstype1Text1','lblCTranstype1Text2','lblCTranstype1Text3'}
sales_price_per_agla_labels                                         = {'lblSSale1SqFt','lblCSale1SqFt1','lblCSale1SqFt2','lblCSale1SqFt3'}
first_floor_area_labels                                             = {'lblSFirstSqFt','lblCFirstSqFt1','lblCFirstSqFt2','lblCFirstSqFt3'}
second_floor_area_labels                                            = {'lblSSecondSqFt','lblCSecondSqFt1','lblCSecondSqFt2','lblCSecondSqFt3'}
half_floor_area_labels                                              = {'lblSHalfSqFt','lblCHalfSqFt1','lblCHalfSqFt2','lblCHalfSqFt3'}
attic_area_labels                                                   = {'lblSAttic','lblCAttic1','lblCAttic2','lblCAttic3'}
other_floor_area_labels                                             = {'lblSOther','lblCOther1','lblCOther2','lblCOther3'}
total_above_ground_living_area_labels                               = {'lblSLowerLevelSize','lblCLowerLevelSize1','lblCLowerLevelSize2','lblCLowerLevelSize3'}
basement_area_labels                                                = {'lblSbasementTTL','lblCbasementTTL1','lblCbasementTTL2','lblCbasementTTL3'}
basement_finished_area_labels                                       = {'lblSFinishLowerLevel','lblCFinishLowerLevel1','lblCFinishLowerLevel2','lblCFinishLowerLevel3'}
lower_level_area_labels                                             = {'lblSLowerTTL','lblCLowerTTL1','lblCLowerTTL2','lblCLowerTTL3'}
lower_level_finished_area_labels                                    = {'lblSLowerFin','lblCLowerFin1','lblCLowerFin2','lblCLowerFin3'}
full_baths_labels                                                   = {'lblSFullBath','lblCFullBath1','lblCFullBath2','lblCFullBath3'}
half_baths_labels                                                   = {'lblSHalfBath','lblCHalfBath1','lblCHalfBath2','lblCHalfBath3'}
total_fixtures_labels                                               = {'lblSFixtures','lblCFixtures1','lblCFixtures2','lblCFixtures3'}
air_conditioning_labels                                             = {'lblSAir','lblCAir1','lblCAir2','lblCAir3'}
fireplaces_labels                                                   = {'lblSFireplace','lblCFireplace1','lblCFireplace2','lblCFireplace3'}
face_brick_labels                                                   = {'lblSFacebrick','lblCFacebrick1','lblCFacebrick2','lblCFacebrick3'}
roof_cover_labels                                                   = {'lblSRoof','lblCRoof1','lblCRoof2','lblCRoof3'}
garage_attached_labels                                              = {'lblSAttGarageCount','lblCAttGarageCount1','lblCAttGarageCount2','lblCAttGarageCount3'}
garage_detached_labels                                              = {'lblSDetGarageCount','lblCDetGarageCount1','lblCDetGarageCount2','lblCDetGarageCount3'}
carport_labels                                                      = {'lblAttCarportCount','lblCAttCarportCount1','lblCAttCarportCount2','lblCAttCarportCount3'}
garage_attached_area_labels                                         = {'lblSAttGarageSize','lblCAttGarageSize1','lblCAttGarageSize2','lblCAttGarageSize3'}
garage_detached_area_labels                                         = {'lblSDetGarageSize','lblCDetGarageSize1','lblCDetGarageSize2','lblCDetGarageSize3'}
carport_area_labels                                                 = {'lblAttCarportSize','lblCAttCarportSize1','lblCAttCarportSize2','lblCAttCarportSize3'}
decks_labels                                                        = {'lblSDeck','lblCDeck1','lblCDeck2','lblCDeck3'}
patio_labels                                                        = {'lblSPatio','lblCPatio1','lblCPatio2','lblCPatio3'}
deck_area_labels                                                    = {'lblSDeckSize','lblCDeckSize1','lblCDeckSize2','lblCDeckSize3'}
patio_area_labels                                                   = {'lblSPatioSize','lblCPatioSize1','lblCPatioSize2','lblCPatioSize3'}
porches_open_labels                                                 = {'lblSOpenPorch','lblCOpenPorch1','lblCOpenPorch2','lblCOpenPorch3'}
porches_enclosed_labels                                             = {'lblSEncPorch','lblCEncPorch1','lblCEncPorch2','lblCEncPorch3'}
porches_open_area_labels                                            = {'lblSOpenPorchSize','lblCOpenPorchSize1','lblCOpenPorchSize2','lblCOpenPorchSize3'}
porches_enclosed_area_labels                                        = {'lblSEncPorchSize','lblCEncPorchSize1','lblCEncPorchSize2','lblCEncPorchSize3'}
pool_labels                                                         = {'lblSPool','lblCPool1','lblCPool2','lblCPool3'}
gazebo_labels                                                       = {'lblSGazebo','lblCGazebo1','lblCGazebo2','lblCGazebo3'}
shed_labels                                                         = {'lblSShed','lblCShed1','lblCShed2','lblCShed3'}
pole_barn_labels                                                    = {'lblSPoleBldg','lblCPoleBldg1','lblCPoleBldg2','lblCPoleBldg3'}

prop_dictionary                                                     = {'subject_property': {'permanent_index_number':                   "#",
                                                                                            'street_address':                           "#",
                                                                                            'neighborhood_number':                      "#",
                                                                                            'neighborhood_name':                        "#",
                                                                                            'land_size':                                "#",
                                                                                            'house_type_code':                          "#",
                                                                                            'structure_type_stories':                   "#",
                                                                                            'exterior_cover':                           "#",
                                                                                            'quality_grade':                            "#",
                                                                                            'condition':                                "#",
                                                                                            'year_built':                               "#",
                                                                                            'effective_age':                            "#",
                                                                                            'land_assessed_value':                      "#",
                                                                                            'building_assessed_value':                  "#",
                                                                                            'total_assessed_value':                     "#",
                                                                                            'land_market_value':                        "#",
                                                                                            'building_market_value':                    "#",
                                                                                            'total_market_value':                       "#",
                                                                                            'primary_land_method':                      "#",
                                                                                            'land_price_per_size_assessed_value':       "#",
                                                                                            'building_price_per_agla_assessed_value':   "#",
                                                                                            'total_value_per_agla_market_value':        "#",
                                                                                            'last_sale_amount':                         "#",
                                                                                            'date_of_sale':                             "#",
                                                                                            'sales_validation':                         "#",
                                                                                            'compulsory_sale':                          "#",
                                                                                            'sales_price_per_agla':                     "#",
                                                                                            'first_floor_area':                         "#",
                                                                                            'second_floor_area':                        "#",
                                                                                            'half_floor_area':                          "#",
                                                                                            'attic_area':                               "#",
                                                                                            'other_floor_area':                         "#",
                                                                                            'total_above_ground_living_area':           "#",
                                                                                            'basement_area':                            "#",
                                                                                            'basement_finished_area':                   "#",
                                                                                            'lower_level_area':                         "#",
                                                                                            'lower_level_finished_area':                "#",
                                                                                            'full_baths':                               "#",
                                                                                            'half_baths':                               "#",
                                                                                            'total_fixtures':                           "#",
                                                                                            'air_conditioning':                         "#",
                                                                                            'fireplaces':                               "#",
                                                                                            'face_brick':                               "#",
                                                                                            'roof_cover':                               "#",
                                                                                            'garage_attached':                          "#",
                                                                                            'garage_detached':                          "#",
                                                                                            'carport':                                  "#",
                                                                                            'garage_attached_area':                     "#",
                                                                                            'garage_detached_area':                     "#",
                                                                                            'carport_area':                             "#",
                                                                                            'decks':                                    "#",
                                                                                            'patio':                                    "#",
                                                                                            'deck_area':                                "#",
                                                                                            'patio_area':                               "#",
                                                                                            'porches_open':                             "#",
                                                                                            'porches_enclosed':                         "#",
                                                                                            'porches_open_area':                        "#",
                                                                                            'porches_enclosed_area':                    "#",
                                                                                            'pool':                                     "#",
                                                                                            'gazebo':                                   "#",
                                                                                            'shed':                                     "#",
                                                                                            'pole_barn':                                "#"},
                                                                        'comp_property_1': {'permanent_index_number':                   "#",
                                                                                            'street_address':                           "#",
                                                                                            'neighborhood_number':                      "#",
                                                                                            'neighborhood_name':                        "#",
                                                                                            'land_size':                                "#",
                                                                                            'house_type_code':                          "#",
                                                                                            'structure_type_stories':                   "#",
                                                                                            'exterior_cover':                           "#",
                                                                                            'quality_grade':                            "#",
                                                                                            'condition':                                "#",
                                                                                            'year_built':                               "#",
                                                                                            'effective_age':                            "#",
                                                                                            'land_assessed_value':                      "#",
                                                                                            'building_assessed_value':                  "#",
                                                                                            'total_assessed_value':                     "#",
                                                                                            'land_market_value':                        "#",
                                                                                            'building_market_value':                    "#",
                                                                                            'total_market_value':                       "#",
                                                                                            'primary_land_method':                      "#",
                                                                                            'land_price_per_size_assessed_value':       "#",
                                                                                            'building_price_per_agla_assessed_value':   "#",
                                                                                            'total_value_per_agla_market_value':        "#",
                                                                                            'last_sale_amount':                         "#",
                                                                                            'date_of_sale':                             "#",
                                                                                            'sales_validation':                         "#",
                                                                                            'compulsory_sale':                          "#",
                                                                                            'sales_price_per_agla':                     "#",
                                                                                            'first_floor_area':                         "#",
                                                                                            'second_floor_area':                        "#",
                                                                                            'half_floor_area':                          "#",
                                                                                            'attic_area':                               "#",
                                                                                            'other_floor_area':                         "#",
                                                                                            'total_above_ground_living_area':           "#",
                                                                                            'basement_area':                            "#",
                                                                                            'basement_finished_area':                   "#",
                                                                                            'lower_level_area':                         "#",
                                                                                            'lower_level_finished_area':                "#",
                                                                                            'full_baths':                               "#",
                                                                                            'half_baths':                               "#",
                                                                                            'total_fixtures':                           "#",
                                                                                            'air_conditioning':                         "#",
                                                                                            'fireplaces':                               "#",
                                                                                            'face_brick':                               "#",
                                                                                            'roof_cover':                               "#",
                                                                                            'garage_attached':                          "#",
                                                                                            'garage_detached':                          "#",
                                                                                            'carport':                                  "#",
                                                                                            'garage_attached_area':                     "#",
                                                                                            'garage_detached_area':                     "#",
                                                                                            'carport_area':                             "#",
                                                                                            'decks':                                    "#",
                                                                                            'patio':                                    "#",
                                                                                            'deck_area':                                "#",
                                                                                            'patio_area':                               "#",
                                                                                            'porches_open':                             "#",
                                                                                            'porches_enclosed':                         "#",
                                                                                            'porches_open_area':                        "#",
                                                                                            'porches_enclosed_area':                    "#",
                                                                                            'pool':                                     "#",
                                                                                            'gazebo':                                   "#",
                                                                                            'shed':                                     "#",
                                                                                            'pole_barn':                                "#"},
                                                                        'comp_property_2': {'permanent_index_number':                   "#",
                                                                                            'street_address':                           "#",
                                                                                            'neighborhood_number':                      "#",
                                                                                            'neighborhood_name':                        "#",
                                                                                            'land_size':                                "#",
                                                                                            'house_type_code':                          "#",
                                                                                            'structure_type_stories':                   "#",
                                                                                            'exterior_cover':                           "#",
                                                                                            'quality_grade':                            "#",
                                                                                            'condition':                                "#",
                                                                                            'year_built':                               "#",
                                                                                            'effective_age':                            "#",
                                                                                            'land_assessed_value':                      "#",
                                                                                            'building_assessed_value':                  "#",
                                                                                            'total_assessed_value':                     "#",
                                                                                            'land_market_value':                        "#",
                                                                                            'building_market_value':                    "#",
                                                                                            'total_market_value':                       "#",
                                                                                            'primary_land_method':                      "#",
                                                                                            'land_price_per_size_assessed_value':       "#",
                                                                                            'building_price_per_agla_assessed_value':   "#",
                                                                                            'total_value_per_agla_market_value':        "#",
                                                                                            'last_sale_amount':                         "#",
                                                                                            'date_of_sale':                             "#",
                                                                                            'sales_validation':                         "#",
                                                                                            'compulsory_sale':                          "#",
                                                                                            'sales_price_per_agla':                     "#",
                                                                                            'first_floor_area':                         "#",
                                                                                            'second_floor_area':                        "#",
                                                                                            'half_floor_area':                          "#",
                                                                                            'attic_area':                               "#",
                                                                                            'other_floor_area':                         "#",
                                                                                            'total_above_ground_living_area':           "#",
                                                                                            'basement_area':                            "#",
                                                                                            'basement_finished_area':                   "#",
                                                                                            'lower_level_area':                         "#",
                                                                                            'lower_level_finished_area':                "#",
                                                                                            'full_baths':                               "#",
                                                                                            'half_baths':                               "#",
                                                                                            'total_fixtures':                           "#",
                                                                                            'air_conditioning':                         "#",
                                                                                            'fireplaces':                               "#",
                                                                                            'face_brick':                               "#",
                                                                                            'roof_cover':                               "#",
                                                                                            'garage_attached':                          "#",
                                                                                            'garage_detached':                          "#",
                                                                                            'carport':                                  "#",
                                                                                            'garage_attached_area':                     "#",
                                                                                            'garage_detached_area':                     "#",
                                                                                            'carport_area':                             "#",
                                                                                            'decks':                                    "#",
                                                                                            'patio':                                    "#",
                                                                                            'deck_area':                                "#",
                                                                                            'patio_area':                               "#",
                                                                                            'porches_open':                             "#",
                                                                                            'porches_enclosed':                         "#",
                                                                                            'porches_open_area':                        "#",
                                                                                            'porches_enclosed_area':                    "#",
                                                                                            'pool':                                     "#",
                                                                                            'gazebo':                                   "#",
                                                                                            'shed':                                     "#",
                                                                                            'pole_barn':                                "#"},
                                                                        'comp_property_3': {'permanent_index_number':                   "#",
                                                                                            'street_address':                           "#",
                                                                                            'neighborhood_number':                      "#",
                                                                                            'neighborhood_name':                        "#",
                                                                                            'land_size':                                "#",
                                                                                            'house_type_code':                          "#",
                                                                                            'structure_type_stories':                   "#",
                                                                                            'exterior_cover':                           "#",
                                                                                            'quality_grade':                            "#",
                                                                                            'condition':                                "#",
                                                                                            'year_built':                               "#",
                                                                                            'effective_age':                            "#",
                                                                                            'land_assessed_value':                      "#",
                                                                                            'building_assessed_value':                  "#",
                                                                                            'total_assessed_value':                     "#",
                                                                                            'land_market_value':                        "#",
                                                                                            'building_market_value':                    "#",
                                                                                            'total_market_value':                       "#",
                                                                                            'primary_land_method':                      "#",
                                                                                            'land_price_per_size_assessed_value':       "#",
                                                                                            'building_price_per_agla_assessed_value':   "#",
                                                                                            'total_value_per_agla_market_value':        "#",
                                                                                            'last_sale_amount':                         "#",
                                                                                            'date_of_sale':                             "#",
                                                                                            'sales_validation':                         "#",
                                                                                            'compulsory_sale':                          "#",
                                                                                            'sales_price_per_agla':                     "#",
                                                                                            'first_floor_area':                         "#",
                                                                                            'second_floor_area':                        "#",
                                                                                            'half_floor_area':                          "#",
                                                                                            'attic_area':                               "#",
                                                                                            'other_floor_area':                         "#",
                                                                                            'total_above_ground_living_area':           "#",
                                                                                            'basement_area':                            "#",
                                                                                            'basement_finished_area':                   "#",
                                                                                            'lower_level_area':                         "#",
                                                                                            'lower_level_finished_area':                "#",
                                                                                            'full_baths':                               "#",
                                                                                            'half_baths':                               "#",
                                                                                            'total_fixtures':                           "#",
                                                                                            'air_conditioning':                         "#",
                                                                                            'fireplaces':                               "#",
                                                                                            'face_brick':                               "#",
                                                                                            'roof_cover':                               "#",
                                                                                            'garage_attached':                          "#",
                                                                                            'garage_detached':                          "#",
                                                                                            'carport':                                  "#",
                                                                                            'garage_attached_area':                     "#",
                                                                                            'garage_detached_area':                     "#",
                                                                                            'carport_area':                             "#",
                                                                                            'decks':                                    "#",
                                                                                            'patio':                                    "#",
                                                                                            'deck_area':                                "#",
                                                                                            'patio_area':                               "#",
                                                                                            'porches_open':                             "#",
                                                                                            'porches_enclosed':                         "#",
                                                                                            'porches_open_area':                        "#",
                                                                                            'porches_enclosed_area':                    "#",
                                                                                            'pool':                                     "#",
                                                                                            'gazebo':                                   "#",
                                                                                            'shed':                                     "#",
                                                                                            'pole_barn':                                "#"}}
                                                    

print("Working from file: " + pinSourceFile)
print(datetime.datetime.now())

def getNextPin(currentPinCounter):

    if (currentPinCounter < len(pinDataSet)):
        nextPin = pinDataSet[currentPinCounter].strip()
        return nextPin[:10]
    else:
        return "0000000000" # should only happen at the end of the file where there is not an even 4 lines to grab

with open(pinSourceFile, 'r') as f:
    for line in f:
        if (line == ""): 
            continue
        pinDataSet.append(line)
        record_counter +=1

#------------------------------------------------------------
# Need to grab 4 pins at a time. There is no association with
# the pins and the data between each.  The DB will be used to
# associate the respective properties.
#------------------------------------------------------------
for x in range(0,(math.ceil(len(pinDataSet)/4))): # divide the lenth of pinDataSet by 4 and round "up"
    #pdb.set_trace()

    subjectpin  = getNextPin(pinCounter) #pinCounter initially set to zero
    pinCounter += 1
    compPin1    = getNextPin(pinCounter)
    pinCounter += 1
    compPin2    = getNextPin(pinCounter)
    pinCounter += 1
    compPin3    = getNextPin(pinCounter)
    pinCounter += 1

    #print (subjectpin, compPin1, compPin2, compPin3)
    #subjectpin, compPin1, compPin2, compPin3 = '0302300025','0302300026','0302300027','0302300028'  
    #pdb.set_trace()

    for x in range(0,10):
            try:
                #print("")
                #print("------------- start URL grab ---------------")
                #print('https://apps03.lakecountyil.gov/comparables/PTAIComp.aspx?' + \
                #    'grid=A&pin=' + subjectpin + '&cmp1pin=' + compPin1 + '&cmp2pin=' +\
                #    compPin2 + '&cmp3pin=' + compPin3)

                startURLRequest = datetime.datetime.now()
                html_contents = requests.get('https://apps03.lakecountyil.gov/comparables/PTAIComp.aspx?' + \
                                              'grid=A&pin=' + subjectpin + '&cmp1pin=' + compPin1 + '&cmp2pin=' +\
                                               compPin2 + '&cmp3pin=' + compPin3, timeout=3).text 
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
                    errorFileToWrite.write('Connection Error while processing: https://apps03.lakecountyil.gov/comparables/PTAIComp.aspx?' + \
                                            'grid=A&pin=' + subjectpin + '&cmp1pin=' + compPin1 + '&cmp2pin=' +\
                                            compPin2 + '&cmp3pin=' + compPin3 + '\r')


                    internetConnectionError_counter +=1
                time.sleep(waitForConnectionTimer)
            finally:
                if internetConnectionError == 9:
                    sys.exit("Internet Connection is not sufficient to keep going.... ending program at time: " + str(datetime.datetime.now()))




    for table in html_soup.find_all('table', id='table2'):
        try:
            #Get PINs
            dataFields = table.find_all(id=permanent_index_number_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            if (invalidPin in str(dataFields)):
                markBadPins = subject + " : " + comp_1 + " : " + comp_2 + " : " + comp_3 #Used later to report an error
            prop_dictionary['subject_property']['permanent_index_number']        = BeautifulSoup(subject, 'html.parser').text 
            prop_dictionary['comp_property_1']['permanent_index_number']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['permanent_index_number']         = BeautifulSoup(comp_2, 'html.parser').text 
            prop_dictionary['comp_property_3']['permanent_index_number']         = BeautifulSoup(comp_3, 'html.parser').text 
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get Street Address
            dataFields = table.find_all(id=street_address_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['street_address']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['street_address']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['street_address']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['street_address']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get neighborhood_number
            dataFields = table.find_all(id=neighborhood_number_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['neighborhood_number']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['neighborhood_number']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['neighborhood_number']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['neighborhood_number']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get neighborhood_name
            dataFields = table.find_all(id=neighborhood_name_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['neighborhood_name']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['neighborhood_name']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['neighborhood_name']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['neighborhood_name']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get land_size
            dataFields = table.find_all(id=land_size_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['land_size']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['land_size']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['land_size']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['land_size']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get house_type_code
            dataFields = table.find_all(id=house_type_code_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['house_type_code']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['house_type_code']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['house_type_code']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['house_type_code']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get structure_type_stories
            dataFields = table.find_all(id=structure_type_stories_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['structure_type_stories']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['structure_type_stories']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['structure_type_stories']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['structure_type_stories']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get exterior_cover
            dataFields = table.find_all(id=exterior_cover_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['exterior_cover']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['exterior_cover']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['exterior_cover']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['exterior_cover']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get quality_grade
            dataFields = table.find_all(id=quality_grade_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['quality_grade']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['quality_grade']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['quality_grade']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['quality_grade']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''
            
            #Get condition
            dataFields = table.find_all(id=condition_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['condition']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['condition']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['condition']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['condition']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get year_built
            dataFields = table.find_all(id=year_built_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['year_built']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['year_built']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['year_built']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['year_built']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get effective_age
            dataFields = table.find_all(id=effective_age_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['effective_age']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['effective_age']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['effective_age']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['effective_age']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get land_assessed_value
            dataFields = table.find_all(id=land_assessed_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['land_assessed_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['land_assessed_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['land_assessed_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['land_assessed_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get building_assessed_value
            dataFields = table.find_all(id=building_assessed_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['building_assessed_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['building_assessed_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['building_assessed_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['building_assessed_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get total_assessed_value
            dataFields = table.find_all(id=total_assessed_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['total_assessed_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['total_assessed_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['total_assessed_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['total_assessed_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get land_market_value
            dataFields = table.find_all(id=land_market_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['land_market_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['land_market_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['land_market_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['land_market_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get building_market_value
            dataFields = table.find_all(id=building_market_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['building_market_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['building_market_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['building_market_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['building_market_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get total_market_value
            dataFields = table.find_all(id=total_market_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['total_market_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['total_market_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['total_market_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['total_market_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get primary_land_method
            dataFields = table.find_all(id=primary_land_method_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['primary_land_method']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['primary_land_method']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['primary_land_method']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['primary_land_method']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get land_price_per_size_assessed_value
            dataFields = table.find_all(id=land_price_per_size_assessed_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['land_price_per_size_assessed_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['land_price_per_size_assessed_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['land_price_per_size_assessed_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['land_price_per_size_assessed_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get building_price_per_agla_assessed_value
            dataFields = table.find_all(id=building_price_per_agla_assessed_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['building_price_per_agla_assessed_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['building_price_per_agla_assessed_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['building_price_per_agla_assessed_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['building_price_per_agla_assessed_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get total_value_per_agla_market_value
            dataFields = table.find_all(id=total_value_per_agla_market_value_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['total_value_per_agla_market_value']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['total_value_per_agla_market_value']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['total_value_per_agla_market_value']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['total_value_per_agla_market_value']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get last_sale_amount
            dataFields = table.find_all(id=last_sale_amount_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['last_sale_amount']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['last_sale_amount']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['last_sale_amount']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['last_sale_amount']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get date_of_sale
            dataFields = table.find_all(id=date_of_sale_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['date_of_sale']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['date_of_sale']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['date_of_sale']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['date_of_sale']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''
            
            #Get sales_validation
            dataFields = table.find_all(id=sales_validation_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').replace("property, e.g., ", '').split(', ')
            prop_dictionary['subject_property']['sales_validation']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['sales_validation']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['sales_validation']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['sales_validation']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

                

            #Get compulsory_sale
            dataFields = table.find_all(id=compulsory_sale_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').replace("away, ",'').split(', ')
            prop_dictionary['subject_property']['compulsory_sale']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['compulsory_sale']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['compulsory_sale']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['compulsory_sale']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get sales_price_per_agla
            dataFields = table.find_all(id=sales_price_per_agla_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['sales_price_per_agla']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['sales_price_per_agla']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['sales_price_per_agla']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['sales_price_per_agla']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get first_floor_area
            dataFields = table.find_all(id=first_floor_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['first_floor_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['first_floor_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['first_floor_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['first_floor_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get second_floor_area
            dataFields = table.find_all(id=second_floor_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['second_floor_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['second_floor_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['second_floor_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['second_floor_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get half_floor_area
            dataFields = table.find_all(id=half_floor_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['half_floor_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['half_floor_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['half_floor_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['half_floor_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get attic_area
            dataFields = table.find_all(id=attic_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['attic_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['attic_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['attic_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['attic_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get other_floor_area
            dataFields = table.find_all(id=other_floor_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['other_floor_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['other_floor_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['other_floor_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['other_floor_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get total_above_ground_living_area
            dataFields = table.find_all(id=total_above_ground_living_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['total_above_ground_living_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['total_above_ground_living_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['total_above_ground_living_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['total_above_ground_living_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get basement_area
            dataFields = table.find_all(id=basement_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['basement_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['basement_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['basement_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['basement_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get basement_finished_area
            dataFields = table.find_all(id=basement_finished_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['basement_finished_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['basement_finished_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['basement_finished_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['basement_finished_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get lower_level_area
            dataFields = table.find_all(id=lower_level_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['lower_level_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['lower_level_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['lower_level_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['lower_level_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get lower_level_finished_area
            dataFields = table.find_all(id=lower_level_finished_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['lower_level_finished_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['lower_level_finished_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['lower_level_finished_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['lower_level_finished_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get full_baths
            dataFields = table.find_all(id=full_baths_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['full_baths']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['full_baths']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['full_baths']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['full_baths']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get half_baths
            dataFields = table.find_all(id=half_baths_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['half_baths']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['half_baths']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['half_baths']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['half_baths']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get total_fixtures
            dataFields = table.find_all(id=total_fixtures_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['total_fixtures']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['total_fixtures']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['total_fixtures']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['total_fixtures']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get air_conditioning
            dataFields = table.find_all(id=air_conditioning_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['air_conditioning']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['air_conditioning']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['air_conditioning']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['air_conditioning']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get fireplaces
            dataFields = table.find_all(id=fireplaces_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['fireplaces']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['fireplaces']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['fireplaces']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['fireplaces']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get face_brick
            dataFields = table.find_all(id=face_brick_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['face_brick']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['face_brick']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['face_brick']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['face_brick']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get roof_cover
            dataFields = table.find_all(id=roof_cover_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['roof_cover']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['roof_cover']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['roof_cover']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['roof_cover']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get garage_attached
            dataFields = table.find_all(id=garage_attached_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['garage_attached']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['garage_attached']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['garage_attached']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['garage_attached']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get garage_detached
            dataFields = table.find_all(id=garage_detached_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['garage_detached']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['garage_detached']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['garage_detached']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['garage_detached']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get carport
            dataFields = table.find_all(id=carport_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['carport']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['carport']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['carport']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['carport']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get garage_attached_area
            dataFields = table.find_all(id=garage_attached_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['garage_attached_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['garage_attached_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['garage_attached_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['garage_attached_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get garage_attached_area
            dataFields = table.find_all(id=garage_attached_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['garage_attached_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['garage_attached_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['garage_attached_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['garage_attached_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get garage_detached_area
            dataFields = table.find_all(id=garage_detached_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['garage_detached_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['garage_detached_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['garage_detached_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['garage_detached_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get carport_area
            dataFields = table.find_all(id=carport_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['carport_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['carport_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['carport_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['carport_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get decks
            dataFields = table.find_all(id=decks_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['decks']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['decks']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['decks']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['decks']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get patio
            dataFields = table.find_all(id=patio_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['patio']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['patio']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['patio']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['patio']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get deck_area
            dataFields = table.find_all(id=deck_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['deck_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['deck_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['deck_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['deck_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get patio_area
            dataFields = table.find_all(id=patio_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['patio_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['patio_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['patio_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['patio_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get porches_open
            dataFields = table.find_all(id=porches_open_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['porches_open']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['porches_open']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['porches_open']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['porches_open']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get porches_enclosed
            dataFields = table.find_all(id=porches_enclosed_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['porches_enclosed']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['porches_enclosed']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['porches_enclosed']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['porches_enclosed']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get porches_open_area
            dataFields = table.find_all(id=porches_open_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['porches_open_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['porches_open_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['porches_open_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['porches_open_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get porches_enclosed_area
            dataFields = table.find_all(id=porches_enclosed_area_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['porches_enclosed_area']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['porches_enclosed_area']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['porches_enclosed_area']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['porches_enclosed_area']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get pool
            dataFields = table.find_all(id=pool_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['pool']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['pool']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['pool']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['pool']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get gazebo
            dataFields = table.find_all(id=gazebo_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['gazebo']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['gazebo']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['gazebo']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['gazebo']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get shed
            dataFields = table.find_all(id=shed_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['shed']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['shed']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['shed']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['shed']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''

            #Get pole_barn
            dataFields = table.find_all(id=pole_barn_labels)
            subject,comp_1,comp_2,comp_3 = str(dataFields).replace('[]','').split(', ')
            prop_dictionary['subject_property']['pole_barn']        = BeautifulSoup(subject, 'html.parser').text
            prop_dictionary['comp_property_1']['pole_barn']         = BeautifulSoup(comp_1, 'html.parser').text 
            prop_dictionary['comp_property_2']['pole_barn']         = BeautifulSoup(comp_2, 'html.parser').text
            prop_dictionary['comp_property_3']['pole_barn']         = BeautifulSoup(comp_3, 'html.parser').text
            subject,comp_1,comp_2,comp_3 = '','','',''
           

        #print(json.dumps(prop_dictionary, indent=4, sort_keys=False))

            recordToWrite = ""
            whichInnerKey = ('subject_property','comp_property_1','comp_property_2','comp_property_3')

            for x in range(0,4):
                #pdb.set_trace()
                for subKey in prop_dictionary[whichInnerKey[x]].values():
                    recordToWrite += subKey.replace('[','').replace(']','').replace(',','').replace('/','-').strip('$') + "|"
                #pdb.set_trace()
                if (invalidPin in recordToWrite):
                    if (prop_dictionary[whichInnerKey[x]]['street_address'] != '0000000000'):
                        errorFileToWrite.write("One of the following PIN number is INVALID: " + (BeautifulSoup(markBadPins, 'html.parser').text) + "\r")
                        pinsInError_counter += 1
                        markBadPins = ''
                        recordToWrite = ''
                
                else:
                    recordToWrite += '\r'
                    dataFileToWrite.write(recordToWrite)
                    recordsWrittenToFile_counter += 1
                    recordToWrite = ""
        except:
            #print("Something when wrong skipping pins... but don't stop the program: " + subjectpin + ", " + compPin1 + ", " + compPin2 + ", " + compPin3 + "\r")         
            pinsInError_counter += 4

#---------------------------------------------
# Show statistics of the program execution
#---------------------------------------------
completionTime = datetime.datetime.now()
print('#-------------------------------------------------------------------')
print('#                        Program Statistics                         ')
print('#-------------------------------------------------------------------')
print("Program execution time in Seconds: " + str((completionTime - startTime).total_seconds()) + '\tRecords/Second:   ' + str((round(((completionTime - startTime).total_seconds()/record_counter),2))))
print("Records read from File:            " + pinSourceFile + '\t\t: ' + str(record_counter))
print("Records written to Data File:      " + dataToWriteFile + '\t: ' + str(recordsWrittenToFile_counter))
print("Records written to Error File:     " + errorFile + '\t: ' + str(pinsInError_counter))
print("\t\t\t\t     Internet Connection Errors "    + ": " + str(internetConnectionError_counter))
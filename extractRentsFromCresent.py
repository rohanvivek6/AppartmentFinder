import requests
import json
import time
from googleSheets import GoogleSheet
from datetime import datetime

class CresentRentExtractor():
	def __init__(self):
		self.baseUrl = "https://www.irvinecompanyapartments.com/snp?sp_q_6=0+1&sp_q_1=unit&sp_x_1=entityType&sp_q_2=ica&sp_x_2=appId&app=ica&count=999&sp_x_3=communityIdAEM&sp_q_3=7d86836c-feda-4653-9a89-c6f4113ec655&sp_x_6=bedroomFilter&sp_q_6=0+1&upm_field_table=1&hide=upm_data&_=1531088964046"
		self.fieldsToExtract = ["floorplanMarketingName","unitMarketingName","unitPricingDate", "unitBestPrice","unitBestTerm", "marketRent", "floorSquareFeet", "floorLevel","bedrooms", "calc_minRent", "calc_pf_minRent", "calc_pf_maxRent", "calc_pf_lowDate"]
		pathToCredentialsFile = 'Appartment hunter-98ec7597dfa6.json'
		spreadSheetName = 'ApartmentHunter'
		self.googleSheet = GoogleSheet(pathToCredentialsFile, spreadSheetName)

	# def getParams(self):
	# 	noOfBedrooms = '0+1'
	# 	params = {}
	# 	params['sp_q_6'] = noOfBedrooms
	# 	return params;

	def extractApartmentDetails(self, appartment):
		appartmentDetails = {}
		for field in self.fieldsToExtract:
			appartmentDetails[field] = appartment[field]
		return appartmentDetails;

	def writeHeaderLine(self):
		self.googleSheet.writeHeaderLine(self.fieldsToExtract)

	def writeAppartmentDetailsToGoogleDoc(self, appartmentDetails):
		rowToWrite = self.googleSheet.getLastPopulatedRow() + 1
		for i in range(len(appartmentDetails)):
			print("Writing test to colm" +str(i) )
			self.googleSheet.writeToCell(rowToWrite, i+1, appartmentDetails[self.fieldsToExtract[i]])
			i = i +1
		self.googleSheet.updateLastPopulatedRow(rowToWrite)

	def getAppartmentsAvaiable(self):
		print("La")
		response = requests.get(self.baseUrl
			# , params = self.getParams()
			);
		if response.status_code == 200 :
			print("here")
			jsonResponse = json.loads(response.text)
			print(response.text)
			appartmentList = jsonResponse['resultsets'][0]['results']
			for appartment in appartmentList :
				appartmentDetails = self.extractApartmentDetails(appartment)
				print("Starting")
				self.writeAppartmentDetailsToGoogleDoc(appartmentDetails)
				print("Done")
		else :
			print ("Error")

todaysDate = datetime.now()
rentExtractor = CresentRentExtractor()
rentExtractor.writeHeaderLine()
rentExtractor.getAppartmentsAvaiable()
# sheet = GoogleSheet(pathToCredentialsFile, 'AppartmentHunter')
# sheet.writeHeaderLine(fieldsToExtract)

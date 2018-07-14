import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet(object):
	"""docstring for GoogleSheet"""
	def __init__(self, pathToCredentialsFile, spreadSheetName):
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		credentials = ServiceAccountCredentials.from_json_keyfile_name(pathToCredentialsFile, scope)
		self.gc = gc = gspread.authorize(credentials)
		self.spreadSheetName = spreadSheetName

	def __getWorkSheet(self):
		try:
			return self.gc.open(self.spreadSheetName).sheet1
		except :
			print("Api Error, sleeping for 100 seconds")
			time.sleep(100)
			return self.gc.open(self.spreadSheetName).sheet1

	def printDoc(self):
		wks = self.__getWorkSheet()
		print(wks.get_all_records())

	def writeHeaderLine(self, headerFields):
		wks = self.__getWorkSheet()
		for i in range(len(headerFields)) :
			wks.update_cell(2, i+1, headerFields[i])

	def writeToCell(self, rowNumber, columnNumber, data):
		wks = self.__getWorkSheet()
		wks.update_cell(rowNumber, columnNumber, data)
		time.sleep(0.5)

	def getLastPopulatedRow(self):
		wks = self.__getWorkSheet()
		return int(wks.acell('A1').value)

	def updateLastPopulatedRow(self, lastUpdatedRowNumber):
		wks = self.__getWorkSheet()
		wks.update_acell('A1', lastUpdatedRowNumber)

pathToCredentialsFile = '/Users/rohan/code/credentials/Appartment hunter-98ec7597dfa6.json'
# sheet = GoogleSheet(pathToCredentialsFile)
# sheet.printDoc()



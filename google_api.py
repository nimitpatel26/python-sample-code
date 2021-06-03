

'''

This file contains code to access Google Drive and Sheet API

'''

from datetime import datetime
import pickle
import os.path
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class GoogleApiConnector:

    # Authenticate with the drive and sheet api services
    def __init__(self):

        self.SCOPES = "google api scopes"
        self.credFile = "location of the JSON credentials file"
        self.tokFile = "file path of the token file (this will be generated, if not present)"
        

        creds = None
        if os.path.exists(self.tokFile):
            with open(self.tokFile, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credFile, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.tokFile, 'wb') as token:
                pickle.dump(creds, token)
       


        self.driveService = build('drive', 'v3', credentials=creds, cache_discovery=False)

        self.sheetService = build('sheets', 'v4', credentials=creds, cache_discovery=False)

    # Gets the list of sheet data within sheetRange from a sheet at a particular url 
    # Sheet range can be something like A:A to get data for entire column A in Google Sheet
    def getSheetData(self, url, sheetRange):

        try:
            sheet = self.sheetService.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.getFileId(url),
                                        range=sheetRange).execute()
            values = result.get('values', [])
            return values

        except Exception as e:
            raise Exception("Unable to get data from the spreadsheet")

    # Extracts fileId from url
    def getFileId(self, url):

        return url.split("/d/")[1].split("/")[0]

    # Gets the last modified date of the file at the url
    def lastModDate(self, url):
        try:
            data = self.driveService.files().get(fileId = self.getFileId(url), fields = "modifiedTime").execute()
            return datetime.strptime(data["modifiedTime"][:-1], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(minutes = 5)
        except Exception as e:
            raise Exception ("Unable to get last modified time for the file")

import os
from .Google import Create_Service
from .models import SheetName


# dict_keys(['spreadsheetId', 'properties', 'sheets', 'spreadsheetUrl'])
# print(sheets_file1)

# print(sheets_file1['spreadsheetUrl'])
# print(sheets_file1['spreadsheetId'])
# print(sheets_file1['sheets'])
# print(sheets_file1['properties'])  # Google Sheets information
def create_sheet():
    FOLDER_PATH = os.getcwd()
    CLIENT_SECRET_FILE = os.path.join(FOLDER_PATH, 'client_secret_1.json')
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

    sheets_file1 = service.spreadsheets().create().execute()
    """
    To specify Google Sheets file basic settings and as well as configure default worksheets
    """
    sheet_body = {
        'properties': {
            'title': 'New Sheet',
            'locale': 'en_US',  # optional
            'autoRecalc': 'HOUR',
            # calculation setting #https://developers.google.com/sheets/api/reference/rest/v4/
            # spreadsheets#RecalculationInterval
            'timeZone': 'America/Los_Angeles'
        }
        ,
        'sheets': [
            {
                'properties': {
                    'title': 'Sales South'
                }
            },
            {
                'properties': {
                    'title': 'Sales North'
                }
            }
        ]
    }
    name = SheetName.objects.filter(name="New Sheet")
    if not name:
        sheets_file2 = service.spreadsheets().create(body=sheet_body).execute()
        s = SheetName(name="New Sheet")
        s.save()
        print(sheets_file2['spreadsheetUrl'])
        print(sheets_file2['spreadsheetId'])
        print(sheets_file2['sheets'])
        print(sheets_file2['properties']['title'])

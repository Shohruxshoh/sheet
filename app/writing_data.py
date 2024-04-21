import os
from .Google import Create_Service


def writing(*args):
    # print(args[0])
    # print(args[1])
    # print(args[2])
    CLIENT_SECRET_FILE = 'client_secret_1.json'
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    spreadsheet_id = '1j7fdBHKL8d3Cwy4lRsu8hXRMDNuqIQyQ3fi6SrR2VEU'
    mySpreadsheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range='Sales South'
    ).execute()
    """
    values.pdate method
    """
    worksheet_name = 'Sales South!'
    cell_range_insert = 'A1'
    values = (
        ('Fayl nomi', 'Key', 'Word'),
        # ('Apple', 'Orange', 'Watermelon')
    )
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': values
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()

    # worksheet_name = 'Sales North!'
    # cell_range_insert = 'A1'
    # values = (
    #     ('Col A', 'Col B', 'Col C'),
    #     ('Apple', 'Orange', 'Watermelon')
    # )
    # value_range_body = {
    #     'majorDimension': 'COLUMNS',
    #     'values': values
    # }
    #
    # service.spreadsheets().values().update(
    #     spreadsheetId=spreadsheet_id,
    #     valueInputOption='USER_ENTERED',
    #     range=worksheet_name + cell_range_insert,
    #     body=value_range_body
    # ).execute()

    """
    values.append
    """

    worksheet_name = 'Sales South!'
    cell_range_insert = 'A2'
    values = (
        args[0],
        args[1],
        args[2]
    )
    value_range_body = {
        'majorDimension': 'COLUMNS',
        'values': values
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()

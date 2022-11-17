from __future__ import print_function

import datetime
import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.


"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""

def add_event(dia, mes, materia):

    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

    except HttpError as error:
        print('An error occurred: %s' % error)

    print(str(datetime.date.today().year)+"-"+str(mes)+"-"+str(dia)+"T8:00:00",)

    event = {
        'summary': materia,
        'description': "prova de "+materia.lower(),
        'start':{
            'dateTime': str(datetime.date.today().year)+"-"+str(mes)+"-"+str(dia)+"T8:00:00",
            'timeZone': "America/Recife"
        },
        'end':{
            # 'dateTime': "2022-11-14T12:30:00",
            # 'dateTime': end,
            'dateTime': str(datetime.date.today().year)+"-"+str(mes)+"-"+str(dia)+"T22:00:00",
            'timeZone': "America/Recife"
        }
    }

    event = service.events().insert(calendarId="primary", body=event).execute()

def get_event(dia, mes, materia):
    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

    except HttpError as error:
        print('An error occurred: %s' % error)

    event = service.events().list(calendarId="primary", q=materia).execute()
    return event
# pip install --upgrade google-api-python-client

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime
try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def insert(planfile, calendarid, studentid):
    global CLIENT_SECRET_FILE
    CLIENT_SECRET_FILE = 'client_secret_'+str(studentid)+'.json'
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    ## Opening the planfile for reading
    lines = []
    with open(planfile) as f:
        for line in f:
            lines.append(line.rstrip('\r\n'))
    ## Preparing the planfile-parsing strucutre
    slutlines = {}
    startlines = {}
    datelines = {}
    dates = {}
    months = {}
    months['jan'] = '01'
    months['feb'] = '02'
    months['mar'] = '03'
    months['apr'] = '04'
    months['maj'] = '05'
    months['jun'] = '06'
    months['jul'] = '07'
    months['aug'] = '08'
    months['sep'] = '09'
    months['okt'] = '10'
    months['nov'] = '11'
    months['dec'] = '12'
    try:
        for i in range(len(lines)):
            if lines[i] == 'mandag':
                startlines['Mandag'] = i + 1
            if lines[i] == 'tirsdag':
                startlines['Tirsdag'] = i + 1
            if lines[i] == 'onsdag':
                startlines['Onsdag'] = i + 1
            if lines[i] == 'torsdag':
                startlines['Torsdag'] = i + 1
            if lines[i] == 'fredag':
                startlines['Fredag'] = i + 1
        datelines['Mandag'] = startlines['Mandag']
        datelines['Tirsdag'] = startlines['Tirsdag']
        datelines['Onsdag'] = startlines['Onsdag']
        datelines['Torsdag'] = startlines['Torsdag']
        datelines['Fredag'] = startlines['Fredag']
        dates['Mandag'] = lines[datelines['Mandag']]
        dates['Tirsdag'] = lines[datelines['Tirsdag']]
        dates['Onsdag'] = lines[datelines['Onsdag']]
        dates['Torsdag'] = lines[datelines['Torsdag']]
        dates['Fredag'] = lines[datelines['Fredag']]
        slutlines['Mandag'] = (startlines['Tirsdag'] - 1)
        slutlines['Tirsdag'] = (startlines['Onsdag'] - 1)
        slutlines['Onsdag'] = (startlines['Torsdag'] - 1)
        slutlines['Torsdag'] = (startlines['Fredag'] - 1)
        slutlines['Fredag'] = len(lines)
        ## Parsing entries with reminders
        for key in startlines:
            for i in range(startlines[key], slutlines[key]):
                if 'Lektie' in lines[i] or 'lektie' in lines[i] or 'Husk' in lines[i] or 'husk' in lines[i]:
                    year = currentYear = datetime.now().year
                    startdate = str(year) + '-' + months[str(dates[key].split('.')[-2]).strip()] + '-' + str(
                        dates[key].split('.')[0]).strip() + 'T07:00:00-00:00'
                    enddate = str(year) + '-' + months[str(dates[key].split('.')[-2]).strip()] + '-' + str(
                        dates[key].split('.')[0]).strip() + 'T08:00:00-00:00'
                    event = {
                        'summary': lines[i],
                        'location': '',
                        'description': '',
                        'start': {
                            'dateTime': startdate,
                            'timeZone': 'Europe/Copenhagen',
                        },
                        'end': {
                            'dateTime': enddate,
                            'timeZone': 'Europe/Copenhagen',
                        },
                        'recurrence': [
                        ],
                        'attendees': [
                        ],
                        'reminders': {
                            'useDefault': False,
                            'overrides': [

                                {'method': 'popup', 'minutes': 16 * 60},
                            ],
                        },
                    }
                    event = service.events().insert(calendarId=calendarid, body=event).execute()
        ## Parsing the general records
        for key in startlines:
            description = ''
            for i in range(startlines[key] + 2, slutlines[key]):
                description = description + str(lines[i]) + '\n'
            year = currentYear = datetime.now().year
            dato = str(dates[key].split('.')[0]).strip()
            if len(dato) == 1:
                dato = '0' + dato
            startdate = str(year) + '-' + months[str(dates[key].split('.')[-2]).strip()] + '-' + dato + 'T07:00:00-00:00'
            enddate = str(year) + '-' + months[str(dates[key].split('.')[-2]).strip()] + '-' + dato + 'T08:00:00-00:00'
            event = {
                'summary': 'Ugeplan info',
                'location': '',
                'description': description,
                'start': {
                    'dateTime': startdate,
                    'timeZone': 'Europe/Copenhagen',
                },
                'end': {
                    'dateTime': enddate,
                    'timeZone': 'Europe/Copenhagen',
                },
                'recurrence': [

                ],
                'attendees': [

                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [

                    ],
                },
            }
            event = service.events().insert(calendarId=calendarid, body=event).execute()
        return '0'
    except:
        return 'Error parsing plan to calendar'
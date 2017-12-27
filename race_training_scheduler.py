#!/usr/bin/env python

from apiclient import discovery
import argparse
from datetime import datetime, timedelta
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import os
import pandas

VERSION = "1.0.0"

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/race_training_scheduler.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = '~/.clients/client_secret.json'
APPLICATION_NAME = 'Race Training Scheduler'

def create_training_event(tday, tsummary):
    tday_str = tday.date().isoformat()
    event = {
        'summary': tsummary,
        'start': {
            'date': tday_str
        },
        'end': {
            'date': tday_str
        } 
    }
    return event

def get_calendar_id(api, calendar_name):
    calendar_list = api.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
        if calendar_name == calendar_list_entry['summary']:
            break
    return calendar_list_entry['id']

def get_credentials(flags=None):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'race_training_scheduler.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(os.path.expanduser(CLIENT_SECRET_FILE),
                                              SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def fix_path(ifilename):
    return os.path.expanduser(os.path.expandvars(ifilename))

def make_description():
    result = []
    result.append("This script takes a race date (YYYY/MM/DD) and a training")
    result.append("schedule and places it in a Google calendar.")
    return " ".join(result)

def run(opts):
    race_day = datetime.strptime(opts.race_day, "%Y/%m/%d")
    day_offset = 6 - race_day.weekday()

    training_schedule = pandas.read_csv(fix_path(opts.training_schedule),
                                        index_col=0)

    num_weeks = training_schedule.shape[0]
    start_day = race_day + timedelta(weeks=-num_weeks, days=day_offset)
    training_day = start_day

    credentials = get_credentials(opts)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    calendar_id = get_calendar_id(service, opts.calendar_name)

    for week, row in training_schedule.iterrows():
        print("Week {}".format(week))
            
        for run in row:
            if opts.debug:
                print(training_day.date().isoformat())
            if run.startswith('Rest'):
                print('Resting')
            else:
                training_event = create_training_event(training_day, run)
                cal_event = service.events().insert(calendarId=calendar_id,
                                                    body=training_event).execute()
                print(run)
                if opts.debug:
                    print(cal_event['id'])

            training_day += timedelta(days=1)

if __name__ == '__main__':
    default_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=make_description(),
                                     formatter_class=default_format,
                                     parents=[tools.argparser])

    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="Debug the program.")
    parser.add_argument("-c", "--cal-name", dest="calendar_name",
                        default="Running",
                        help="Set the name of the Google Calendar")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(VERSION))
    parser.add_argument("race_day", help="The date of the race in YYYY/MM/DD"
                        " format")
    parser.add_argument("training_schedule", help="The training schedule to"
                        "ingest. Should be in CSV format.")

    args = parser.parse_args()

    run(args)
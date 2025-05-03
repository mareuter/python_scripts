#!/usr/bin/env python

import argparse
from datetime import datetime, timedelta
import os

from apiclient import discovery
import httplib2
from oauth2client import client, tools
from oauth2client.file import Storage
import pandas

VERSION = "1.0.0"

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/race_training_scheduler.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = '~/.clients/client_secret.json'
APPLICATION_NAME = 'Race Training Scheduler'


def create_training_event(tday, tsummary):
    """Create a training event dictionary.

    Parameters
    ----------
    tday : datetime
        The date/time object for the current training event.
    tsummary : str
        The training event activity.

    Returns
    -------
    dict
        The event information in dictionary form.

    """
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


def find_start_day(rday, tschedule):
    """Find training start day from knowing the race day and training schedule.

    Parameters
    ----------
    rday : str
        The race day in YYYY/MM/DD format.
    tschedule : pandas.DataFrame
        The object containing the training schedule.

    Returns
    -------
    datetime
        The object containing the training start day.

    """
    race_day = datetime.strptime(rday, "%Y/%m/%d")
    day_offset = 6 - race_day.weekday()

    num_weeks = tschedule.shape[0]
    start_day = race_day + timedelta(weeks=-num_weeks, days=day_offset)
    return start_day


def get_calendar_id(api, calendar_name):
    """Get the Id for the requested calendar.

    Parameters
    ----------
    api : Resource
        The object representing the API.
    calendar_name : str
        The text name of the requested calendar.

    Returns
    -------
    str
        The Id of the requested calendar.

    """
    calendar_list = api.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
        if calendar_name == calendar_list_entry['summary']:
            break
    return calendar_list_entry['id']


def get_credentials(flags):
    """Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Parameters
    ----------
    flags : namespace
        The object containing the command-line arguments.

    Returns
    -------
    Credentials
        The obtained credential.

    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'race_training_scheduler.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(os.path.expanduser(CLIENT_SECRET_FILE), SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def fix_path(ifilename):
    """Expand all special markers in a path.

    Parameters
    ----------
    ifilename : str
        The current path, possibly containing special markers.

    Returns
    -------
    str
        The current path with the special markers expanded to path elements.

    """
    return os.path.expanduser(os.path.expandvars(ifilename))


def make_description():
    """Create the program description paragraph.

    Returns
    -------
    str
        The program description paragraph.

    """
    result = []
    result.append("This script takes a race date (YYYY/MM/DD) and a training schedule and places it in ")
    result.append("a Google calendar. The training schedule should be in CSV format with 7 columns. The ")
    result.append("number of rows should be the number of weeks in the training program plus one for the ")
    result.append("days of the week column header at the top of the file.")
    return " ".join(result)


def run(opts):
    """Run the main program elements.

    Parameters
    ----------
    opts : namespace
        The object containing the options from the command-line.

    """
    training_schedule = pandas.read_csv(fix_path(opts.training_schedule), index_col=0)
    training_day = find_start_day(opts.race_day, training_schedule)

    if opts.start_only:
        print("Training Start:", training_day.strftime("%Y-%m-%d"))
        return

    credentials = get_credentials(opts)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    calendar_id = get_calendar_id(service, opts.calendar_name)

    for week, row in training_schedule.iterrows():
        print(f"Week {week}")

        for run in row:
            if opts.debug:
                print(training_day.date().isoformat())
            if run.startswith('Rest'):
                print('Resting')
            else:
                training_event = create_training_event(training_day, run)
                cal_event = service.events().insert(calendarId=calendar_id, body=training_event).execute()
                print(run)
                if opts.debug:
                    print(cal_event['id'])

            training_day += timedelta(days=1)


if __name__ == '__main__':
    default_format = argparse.ArgumentDefaultsHelpFormatter
    # The parents keyword needs to be used in order to add command-line arguments from the OAuth2 package.
    parser = argparse.ArgumentParser(description=make_description(), formatter_class=default_format,
                                     parents=[tools.argparser])

    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="Debug the program.")
    parser.add_argument("-c", "--cal-name", dest="calendar_name", default="Running",
                        help="Set the name of the Google Calendar")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {VERSION}")
    parser.add_argument("-s", "--start-only", dest="start_only", action="store_true",
                        help="Print the training start day and exit.")
    parser.add_argument("race_day", help="The date of the race in YYYY/MM/DD format")
    parser.add_argument("training_schedule", help="The training schedule to ingest. Should be in CSV format.")

    args = parser.parse_args()

    run(args)

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    # print("\n\n", service.calendarList(), "\n\n")
    # print("\n\n", service.calendarList().list().execute(), "\n\n")


    # To get calendar list
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print("summary : ", calendar_list_entry['summary'], " // id : ", calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    maxResult = 1000
    print(f'Getting the upcoming {maxResult} events\n')
    events_result = service.events().list(calendarId='khtks@naver.com', timeMin=datetime.datetime(2020,1,1).isoformat() + 'Z',
                                        timeMax=datetime.datetime(2020,2,28).isoformat() + 'Z',
                                        maxResults=maxResult, singleEvents=True, showDeleted=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        summary = event['summary']
        print(event)
        # print(event['summary'], event['creator'].get('email'), event['start'], event['end'])
        # if "휴가" in summary:
        #     print(event['summary'], event['creator'].get('email'), event['start'], event['end'])
        # if "연차" in summary:
        #     print(event['summary'], event['creator'].get('email'), event['start'], event['end'])
        # if "반차" in summary:
        #     print(event['summary'], event['creator'].get('email'), event['start'], event['end'])
        # if "대체휴가" in summary:
        #     print(event['summary'], event['creator'].get('email'), event['start'], event['end'])

if __name__ == '__main__':
    main()
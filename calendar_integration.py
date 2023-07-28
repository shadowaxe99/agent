import os
import datetime
import unittest
from unittest.mock import patch, MagicMock
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import json

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Expected environment variable '{var_name}' not set."
        raise Exception(error_msg)

def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                get_env_variable('CREDENTIALS_JSON'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"Error building Google Calendar service: {e}")
        return None

    return service

class TestGetCalendarService(unittest.TestCase):
    @patch('googleapiclient.discovery.build')
    def test_get_calendar_service(self, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        self.assertEqual(get_calendar_service(), mock_service)

# Uncomment to run the unit test
# if __name__ == "__main__":
#     unittest.main()
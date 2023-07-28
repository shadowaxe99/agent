import os
import datetime
from googleapiclient.discovery import build

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Expected environment variable '{var_name}' not set."
        raise Exception(error_msg)

def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    try:
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=n, singleEvents=True,
                                            orderBy='startTime').execute()
    except Exception as e:
        print(f"Error getting events: {e}")
        return None

    return events_result.get('items', [])
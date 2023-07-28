import os
import unittest
from twilio.rest import Client
from openai import OpenAI

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Expected environment variable '{var_name}' not set."
        raise Exception(error_msg)

def setup_clients():
    try:
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = get_env_variable('TWILIO_ACCOUNT_SID')
        auth_token = get_env_variable('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
    except Exception as e:
        print(f"Error setting up Twilio client: {e}")
        return None, None

    try:
        openai.api_key = get_env_variable('OPENAI_API_KEY')
    except Exception as e:
        print(f"Error setting up OpenAI client: {e}")
        return None, None

    return client, openai

class TestGetEnvVariable(unittest.TestCase):
    def test_get_env_variable(self):
        os.environ["TEST_VARIABLE"] = "TEST_VALUE"
        self.assertEqual(get_env_variable("TEST_VARIABLE"), "TEST_VALUE")

# Uncomment to run the unit test
# if __name__ == "__main__":
#     unittest.main()
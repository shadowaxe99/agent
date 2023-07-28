import os
import unittest
from unittest.mock import patch, MagicMock
import requests

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Expected environment variable '{var_name}' not set."
        raise Exception(error_msg)

def list_repos(user, token):
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/users/{user}/repos'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return None
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
        return None

    return response.json()

class TestGithubIntegration(unittest.TestCase):
    @patch('requests.get')
    def test_list_repos(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = ['Repo1', 'Repo2']
        mock_get.return_value = mock_response
        self.assertEqual(list_repos('test_user', 'test_token'), ['Repo1', 'Repo2'])

# Uncomment to run the unit tests
# if __name__ == "__main__":
#     unittest.main()
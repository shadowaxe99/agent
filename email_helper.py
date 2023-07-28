import os
import smtplib
import ssl
import unittest
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from unittest.mock import patch

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Expected environment variable '{var_name}' not set."
        raise Exception(error_msg)

def send_email(receiver_email, subject, text):
    # Sender email and password
    sender_email = get_env_variable('SENDER_EMAIL')
    password = get_env_variable('SENDER_PASSWORD')

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(text, 'plain'))

    try:
        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f'Error sending email: {e}')

class TestSendEmail(unittest.TestCase):
    @patch('smtplib.SMTP_SSL')
    def test_send_email(self, mock_smtp):
        receiver_email = 'test@example.com'
        subject = 'Test Subject'
        text = 'Test Email'
        send_email(receiver_email, subject, text)
        mock_smtp.assert_called_once_with('smtp.gmail.com', 465, context=ssl.create_default_context())
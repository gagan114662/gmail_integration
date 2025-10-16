import base64
import email
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
from config import Config

class EmailProcessor:
    """Process and parse Gmail messages"""

    def __init__(self, gmail_service):
        self.service = gmail_service

    def get_message(self, message_id):
        """
        Fetch a specific email message by ID

        Args:
            message_id: Gmail message ID

        Returns:
            dict: Message data
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            return message
        except HttpError as error:
            print(f"Error fetching message {message_id}: {error}")
            return None

    def get_message_body(self, message):
        """
        Extract message body from Gmail message

        Args:
            message: Gmail message object

        Returns:
            str: Message body text
        """
        if 'payload' not in message:
            return ""

        payload = message['payload']

        # Check for simple body
        if 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        # Check for multipart message
        if 'parts' in payload:
            return self._get_multipart_body(payload['parts'])

        return ""

    def _get_multipart_body(self, parts):
        """
        Extract body from multipart message

        Args:
            parts: List of message parts

        Returns:
            str: Combined message body
        """
        body = ""

        for part in parts:
            mime_type = part.get('mimeType', '')

            # Recursively handle nested parts
            if 'parts' in part:
                body += self._get_multipart_body(part['parts'])
            elif mime_type == 'text/plain' and 'data' in part.get('body', {}):
                # Decode text/plain part
                text = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                body += text
            elif mime_type == 'text/html' and not body and 'data' in part.get('body', {}):
                # Fallback to HTML if no plain text found
                html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                body += html

        return body

    def get_message_headers(self, message):
        """
        Extract headers from Gmail message

        Args:
            message: Gmail message object

        Returns:
            dict: Dictionary of headers
        """
        headers = {}

        if 'payload' in message and 'headers' in message['payload']:
            for header in message['payload']['headers']:
                headers[header['name']] = header['value']

        return headers

    def is_signal_email(self, message):
        """
        Check if email contains the signal identifier

        Args:
            message: Gmail message object

        Returns:
            bool: True if message is a signal email
        """
        # Get headers
        headers = self.get_message_headers(message)
        subject = headers.get('Subject', '')

        # Get body
        body = self.get_message_body(message)

        # Check if signal identifier is present
        signal_id = Config.SIGNAL_IDENTIFIER
        return signal_id in subject or signal_id in body

    def get_message_summary(self, message):
        """
        Get a summary of the message for logging

        Args:
            message: Gmail message object

        Returns:
            dict: Message summary
        """
        headers = self.get_message_headers(message)

        return {
            'id': message.get('id'),
            'threadId': message.get('threadId'),
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', ''),
            'snippet': message.get('snippet', '')
        }

    def get_history(self, start_history_id):
        """
        Get message history since a specific history ID

        Args:
            start_history_id: Starting history ID

        Returns:
            list: List of history records
        """
        try:
            history = self.service.users().history().list(
                userId='me',
                startHistoryId=start_history_id,
                historyTypes=['messageAdded']
            ).execute()

            return history.get('history', [])
        except HttpError as error:
            print(f"Error fetching history: {error}")
            return []

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import Config

class GmailAuthenticator:
    """Handle Gmail API authentication using OAuth2"""

    def __init__(self):
        self.creds = None
        self.service = None
        self.token_file = 'token.json'
        self.credentials_file = 'credentials.json'

    def authenticate(self):
        """Authenticate and return Gmail API service"""

        # Load existing token if available
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, Config.GMAIL_SCOPES)

        # If there are no valid credentials, authenticate
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh the token
                self.creds.refresh(Request())
            else:
                # Create credentials from environment variables or credentials.json
                if Config.GMAIL_CLIENT_ID and Config.GMAIL_CLIENT_SECRET:
                    # Use environment variables
                    client_config = {
                        "installed": {
                            "client_id": Config.GMAIL_CLIENT_ID,
                            "client_secret": Config.GMAIL_CLIENT_SECRET,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": ["http://localhost"]
                        }
                    }
                    flow = InstalledAppFlow.from_client_config(client_config, Config.GMAIL_SCOPES)
                elif os.path.exists(self.credentials_file):
                    # Use credentials.json file
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, Config.GMAIL_SCOPES)
                else:
                    raise ValueError("No Gmail credentials found. Please provide credentials.json or set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET")

                self.creds = flow.run_local_server(port=8080)

            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

        # Build Gmail API service
        self.service = build('gmail', 'v1', credentials=self.creds)
        return self.service

    def get_service(self):
        """Get authenticated Gmail API service"""
        if not self.service:
            self.authenticate()
        return self.service

    def setup_push_notifications(self, topic_name, label_ids=None):
        """
        Set up Gmail push notifications via Cloud Pub/Sub

        Args:
            topic_name: Full Pub/Sub topic name (e.g., 'projects/my-project/topics/gmail-push')
            label_ids: List of label IDs to watch (default: ['INBOX'])
        """
        if not self.service:
            self.authenticate()

        if label_ids is None:
            label_ids = ['INBOX']

        request_body = {
            'labelIds': label_ids,
            'topicName': topic_name
        }

        try:
            watch_response = self.service.users().watch(userId='me', body=request_body).execute()
            print(f"Push notifications enabled. History ID: {watch_response.get('historyId')}")
            print(f"Expiration: {watch_response.get('expiration')}")
            return watch_response
        except Exception as e:
            print(f"Error setting up push notifications: {e}")
            raise

    def stop_push_notifications(self):
        """Stop Gmail push notifications"""
        if not self.service:
            self.authenticate()

        try:
            self.service.users().stop(userId='me').execute()
            print("Push notifications stopped")
        except Exception as e:
            print(f"Error stopping push notifications: {e}")
            raise

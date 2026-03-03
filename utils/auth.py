"""
Authentication utilities for Gmail API
"""

import os
import pickle
import json
from typing import Optional
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config.settings import SCOPES, CREDENTIALS_PATH, TOKEN_PATH


def authenticate_gmail():
    """
    Authenticate with Gmail API using OAuth 2.0

    Returns:
        Gmail API service object
    """
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, request authorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                # If refresh fails, delete the token and start fresh
                if os.path.exists(TOKEN_PATH):
                    os.remove(TOKEN_PATH)
                creds = None

        if not creds:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"Credentials file not found at {CREDENTIALS_PATH}. "
                    f"Please follow the setup instructions to create credentials."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    # Build and return the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service


def validate_credentials():
    """
    Validate that credentials are properly set up

    Returns:
        bool: True if credentials are valid, False otherwise
    """
    try:
        service = authenticate_gmail()
        # Try a simple API call to validate credentials
        service.users().getProfile(userId='me').execute()
        return True
    except Exception as e:
        print(f"Error validating credentials: {e}")
        return False
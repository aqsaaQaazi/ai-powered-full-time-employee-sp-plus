import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scope: read-only access (change later if needed for modify)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    # Load from token.json if exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no/invalid creds, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Point to your credentials.json (update path if not in same folder!)
            flow = InstalledAppFlow.from_client_secrets_file(
                r'./credentials.json', SCOPES)  # ← CHANGE THIS PATH
            creds = flow.run_local_server(port=0)
        
        # Save token for future runs
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        # Simple test: list your Gmail labels
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])
    except HttpError as error:
        print(f'API error: {error}')

if __name__ == '__main__':
    main()
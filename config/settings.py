"""
Configuration settings for Gmail Watcher
"""

import os
from pathlib import Path

# Default configuration values
DEFAULT_POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', '120'))  # seconds
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH', './credentials.json')
TOKEN_PATH = os.getenv('TOKEN_PATH', './token.json')
ACTION_DIR = os.getenv('ACTION_DIR', './Needs_Action/')
PROCESSED_EMAILS_PATH = os.getenv('PROCESSED_EMAILS_PATH', './data/.processed_emails.json')

# Keywords to watch for in emails
KEYWORDS = [
    'invoice',
    'urgent',
    'payment',
    'asap',
    'quote',
    'help', 
    "Invoice",
    "Urgent",
    "Payment",
    "ASAP",
    "Quote",
    "Help",
    "INVOICE",
    "URGENT",
    "PAYMENT",
    "ASAP",
    "QUOTE",
    "HELP",
]

# API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

# Priority levels based on keyword matches
HIGH_PRIORITY_KEYWORDS = ['urgent', 'asap', 'help']
MEDIUM_PRIORITY_KEYWORDS = ['invoice', 'payment', 'quote']

# Create action directory if it doesn't exist
Path(ACTION_DIR).mkdir(exist_ok=True)
Path('./data').mkdir(exist_ok=True)
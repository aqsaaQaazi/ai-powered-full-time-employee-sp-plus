"""
Configuration settings for Approval Workflow
"""

import os
from pathlib import Path

# Directory paths
PENDING_APPROVAL_DIR = Path(os.getenv('PENDING_APPROVAL_DIR', './Pending_Approval'))
APPROVED_DIR = Path(os.getenv('APPROVED_DIR', './Approved'))
REJECTED_DIR = Path(os.getenv('REJECTED_DIR', './Rejected'))
LOGS_DIR = Path(os.getenv('LOGS_DIR', './Logs'))

# Create directories if they don't exist
PENDING_APPROVAL_DIR.mkdir(exist_ok=True)
APPROVED_DIR.mkdir(exist_ok=True)
REJECTED_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Approval expiration settings
APPROVAL_EXPIRATION_HOURS = int(os.getenv('APPROVAL_EXPIRATION_HOURS', 24))

# Watchdog settings
WATCHDOG_TIMEOUT = float(os.getenv('WATCHDOG_TIMEOUT', '1.0'))

# Supported action types
SUPPORTED_ACTION_TYPES = [
    'email_send',
    'linkedin_post',
    'payment_draft',
    'social_media_post',
    'file_share',
    'api_call'
]

# Required details for each action type
REQUIRED_DETAILS = {
    'email_send': ['to', 'subject', 'body_preview'],
    'linkedin_post': ['content_preview', 'audience'],
    'payment_draft': ['amount', 'recipient', 'reason'],
    'social_media_post': ['platform', 'content_preview'],
    'file_share': ['recipient', 'file_path', 'permissions'],
    'api_call': ['endpoint', 'method', 'payload_preview']
}
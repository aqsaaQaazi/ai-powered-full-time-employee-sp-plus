"""
Email processing utilities for Gmail Watcher
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
from config.settings import KEYWORDS, HIGH_PRIORITY_KEYWORDS, MEDIUM_PRIORITY_KEYWORDS


def extract_email_metadata(message_data: Dict) -> Dict:
    """
    Extract metadata from Gmail message data

    Args:
        message_data: Raw message data from Gmail API

    Returns:
        Dictionary containing extracted metadata
    """
    headers = {header['name']: header['value'] for header in message_data.get('payload', {}).get('headers', [])}

    # Extract relevant headers
    sender = headers.get('From', 'Unknown Sender')
    subject = headers.get('Subject', 'No Subject')

    # Extract received time
    internal_date = message_data.get('internalDate')
    if internal_date:
        # Convert from milliseconds to seconds
        received_timestamp = int(internal_date) / 1000
        received = datetime.fromtimestamp(received_timestamp).isoformat()
    else:
        received = datetime.now().isoformat()

    # Extract snippet
    snippet = message_data.get('snippet', '')

    return {
        'id': message_data['id'],
        'from': sender,
        'subject': subject,
        'received': received,
        'snippet': snippet
    }


def detect_keywords(text: str) -> List[str]:
    """
    Detect keywords in email text

    Args:
        text: Text to search for keywords

    Returns:
        List of matched keywords
    """
    text_lower = text.lower()
    matched_keywords = []

    for keyword in KEYWORDS:
        if keyword.lower() in text_lower:
            matched_keywords.append(keyword)

    return matched_keywords


def determine_priority(snippet: str, subject: str) -> str:
    """
    Determine email priority based on keyword analysis

    Args:
        snippet: Email snippet
        subject: Email subject

    Returns:
        Priority level ('high', 'medium', 'low')
    """
    combined_text = f"{subject} {snippet}"

    # Check for high priority keywords
    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword.lower() in combined_text.lower():
            return 'high'

    # Check for medium priority keywords
    for keyword in MEDIUM_PRIORITY_KEYWORDS:
        if keyword.lower() in combined_text.lower():
            return 'medium'

    # Default to low priority
    return 'low'


def generate_suggested_actions(priority: str, keywords: List[str]) -> List[str]:
    """
    Generate suggested actions based on email priority and keywords

    Args:
        priority: Email priority level
        keywords: List of keywords found in email

    Returns:
        List of suggested actions
    """
    actions = []

    if 'invoice' in keywords:
        actions.extend([
            "Review invoice details",
            "Process payment if approved",
            "Forward to accounting department"
        ])
    elif 'payment' in keywords:
        actions.extend([
            "Verify payment details",
            "Process payment request",
            "Confirm payment receipt"
        ])
    elif 'urgent' in keywords or priority == 'high':
        actions.extend([
            "Respond to sender immediately",
            "Escalate to manager if needed",
            "Take immediate action required"
        ])
    elif 'asap' in keywords:
        actions.extend([
            "Address request as soon as possible",
            "Schedule time to handle this today",
            "Notify relevant team members"
        ])
    elif 'quote' in keywords:
        actions.extend([
            "Review quote details",
            "Compare with other quotes if available",
            "Decide whether to accept or negotiate"
        ])
    elif 'help' in keywords:
        actions.extend([
            "Assess the help request",
            "Provide assistance or redirect to appropriate person",
            "Follow up to ensure issue is resolved"
        ])
    else:
        actions.extend([
            "Review email content",
            "Determine appropriate response",
            "Take necessary action",
            "Mark as completed when done"
        ])

    return actions
"""
File handling utilities for Gmail Watcher
"""

import os
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from config.settings import ACTION_DIR


def create_actionable_item(email_data: Dict[str, Any]) -> str:
    """
    Create an actionable item markdown file from email data

    Args:
        email_data: Dictionary containing email metadata and processing info

    Returns:
        Path to created file
    """
    # Create file name with EMAIL_[id].md format
    file_name = f"EMAIL_{email_data['id']}.md"
    file_path = os.path.join(ACTION_DIR, file_name)

    # Prepare YAML frontmatter data
    yaml_frontmatter = {
        'type': 'email',
        'from': email_data['from'],
        'subject': email_data['subject'],
        'received': email_data['received'],
        'priority': email_data['priority'],
        'snippet': email_data['snippet'],
        'keywords_found': email_data.get('keywords_found', []),
        'created_at': datetime.now().isoformat(),
        'status': 'pending'
    }

    # Generate suggested actions
    actions = email_data.get('actions', [])

    # Create markdown content
    markdown_content = f"""---
{yaml.dump(yaml_frontmatter, default_flow_style=False)}
---

# {email_data['subject']}

From: {email_data['from']}
Received: {email_data['received']}

## Suggested Actions
"""
    for action in actions:
        markdown_content += f"- [ ] {action}\n"

    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return file_path


def load_processed_emails(file_path: str) -> Dict[str, Any]:
    """
    Load processed email IDs from JSON file

    Args:
        file_path: Path to the processed emails file

    Returns:
        Dictionary containing processed email data
    """
    if not os.path.exists(file_path):
        # Create the file with default structure if it doesn't exist
        default_data = {
            'processed_ids': [],
            'last_updated': datetime.now().isoformat(),
            'version': '1.0'
        }
        save_processed_emails(default_data, file_path)
        return default_data

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        # If file is corrupted, return default data
        print(f"Warning: Could not decode {file_path}, creating default data")
        default_data = {
            'processed_ids': [],
            'last_updated': datetime.now().isoformat(),
            'version': '1.0'
        }
        return default_data


def save_processed_emails(data: Dict[str, Any], file_path: str):
    """
    Save processed email IDs to JSON file

    Args:
        data: Dictionary containing processed email data
        file_path: Path to save the processed emails file
    """
    data['last_updated'] = datetime.now().isoformat()

    # Ensure the directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def is_email_processed(email_id: str, file_path: str) -> bool:
    """
    Check if an email has already been processed

    Args:
        email_id: The email ID to check
        file_path: Path to the processed emails file

    Returns:
        True if email has been processed, False otherwise
    """
    data = load_processed_emails(file_path)
    return email_id in data.get('processed_ids', [])


def mark_email_as_processed(email_id: str, file_path: str):
    """
    Mark an email as processed

    Args:
        email_id: The email ID to mark as processed
        file_path: Path to the processed emails file
    """
    data = load_processed_emails(file_path)

    if email_id not in data.get('processed_ids', []):
        data.setdefault('processed_ids', []).append(email_id)
        data['last_updated'] = datetime.now().isoformat()
        save_processed_emails(data, file_path)


def validate_markdown_file(file_path: str) -> bool:
    """
    Validate that a markdown file has proper structure

    Args:
        file_path: Path to the markdown file to validate

    Returns:
        True if file has valid structure, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file starts with YAML frontmatter
        if not content.startswith('---'):
            return False

        # Look for the end of YAML frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False

        # Basic validation: ensure essential fields are present in YAML
        yaml_content = parts[1]
        required_fields = ['type', 'from', 'subject', 'received', 'priority']

        for field in required_fields:
            if f'{field}:' not in yaml_content:
                return False

        return True
    except Exception:
        return False
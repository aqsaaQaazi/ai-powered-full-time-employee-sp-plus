"""
Approval request parser for Approval Workflow
"""

import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def parse_approval_request(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Parse an approval request file and validate its structure.

    Args:
        file_path: Path to the approval request file

    Returns:
        Dictionary containing approval request data or None if invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split the content to separate YAML frontmatter from markdown body
        parts = content.split('---', 2)

        if len(parts) < 3:
            logger.error(f"Invalid format: {file_path} - missing YAML frontmatter")
            return None

        yaml_content = parts[1].strip()
        markdown_body = parts[2].strip()

        # Parse YAML frontmatter
        try:
            yaml_data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in {file_path}: {e}")
            return None

        # Validate required fields
        if not validate_approval_request_format(yaml_data):
            logger.error(f"Invalid approval request format in {file_path}")
            return None

        # Validate expiration
        if not is_approval_valid(yaml_data):
            logger.warning(f"Approval request has expired: {file_path}")
            return None

        # Combine YAML data with markdown body
        result = yaml_data.copy()
        result['markdown_body'] = markdown_body
        result['file_path'] = str(file_path)
        result['filename'] = file_path.name

        return result

    except Exception as e:
        logger.error(f"Error parsing approval request {file_path}: {e}")
        return None


def validate_approval_request_format(data: Dict[str, Any]) -> bool:
    """
    Validate the structure and content of an approval request.

    Args:
        data: Approval request data dictionary

    Returns:
        True if valid, False otherwise
    """
    # Check required fields
    required_fields = ['type', 'action', 'details', 'created', 'expires']
    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required field: {field}")
            return False

    # Validate type
    if data['type'] != 'approval_request':
        logger.error(f"Invalid type: {data['type']}, expected 'approval_request'")
        return False

    # Validate action
    if not isinstance(data['action'], str) or not data['action']:
        logger.error("Action must be a non-empty string")
        return False

    # Validate details
    if not isinstance(data['details'], dict):
        logger.error("Details must be a dictionary")
        return False

    # Validate timestamps
    try:
        
        # Ensure timestamps are strings before replace
        if not isinstance(data['created'], str):
            logger.error("Created timestamp must be a string")
            return False
        if not isinstance(data['expires'], str):
            logger.error("Expires timestamp must be a string")
            return False
        
        
        created_time = datetime.fromisoformat(data['created'].replace('Z', '+00:00'))
        expires_time = datetime.fromisoformat(data['expires'].replace('Z', '+00:00'))

        current_time = datetime.now(created_time.tzinfo)
        if created_time > current_time:
            logger.error("Created timestamp is in the future")
            return False

        if expires_time < current_time:
            logger.warning("Approval request has expired")
            return False  # Consider expired as invalid for processing

        if (expires_time - created_time).total_seconds() > 25 * 3600:  # More than 25 hours
            logger.error("Expiration period exceeds reasonable limit")
            return False
    except ValueError as e:
        logger.error(f"Invalid timestamp format: {e}")
        return False
    except TypeError as e:
        logger.error(f"Type error in timestamp validation: {e}")
        return False
    return True


def is_approval_valid(data: Dict[str, Any]) -> bool:
    """
    Check if an approval request is still valid (not expired).

    Args:
        data: Approval request data dictionary

    Returns:
        True if valid, False if expired
    """
    try:
        
        # Ensure expires is a string before replace
        if not isinstance(data['expires'], str):
            logger.error("Expires timestamp must be a string")
            return False
        
        expires_time = datetime.fromisoformat(data['expires'].replace('Z', '+00:00'))
        current_time = datetime.now(expires_time.tzinfo)

        return expires_time >= current_time
    
    except ValueError as e:
        logger.error(f"Invalid expiration timestamp format: {e}")
        return False
    
    except TypeError as e:
        logger.error(f"Type error in expiration validation: {e}")
        return False


def create_approval_request_file(
    file_path: Path,
    action_type: str,
    details: Dict[str, Any],
    markdown_body: str
) -> bool:
    """
    Create a new approval request file with proper format.

    Args:
        file_path: Path to create the approval request file
        action_type: Type of action requiring approval
        details: Dictionary containing action details
        markdown_body: Human-readable markdown content

    Returns:
        True if successful, False otherwise
    """
    try:
        from config.settings import APPROVAL_EXPIRATION_HOURS

        # Create timestamp data
        created_time = datetime.now()
        expires_time = created_time + timedelta(hours=APPROVAL_EXPIRATION_HOURS)

        # Format as ISO strings
        created_str = created_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        expires_str = expires_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Construct YAML frontmatter
        yaml_data = {
            'type': 'approval_request',
            'action': action_type,
            'details': details,
            'created': created_str,
            'expires': expires_str
        }

        # Create the content
        content = f"""---
{yaml.dump(yaml_data, default_flow_style=False)}
---
{markdown_body}
"""

        # Write to file
        from utils.file_operations import safe_write_to_file
        return safe_write_to_file(file_path, content)

    except Exception as e:
        logger.error(f"Error creating approval request file {file_path}: {e}")
        return False


from datetime import timedelta
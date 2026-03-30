"""
Action executor for Approval Workflow
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def execute_approved_action(approval_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute an approved action based on its type and details.

    Args:
        approval_data: Dictionary containing approval request data

    Returns:
        Dictionary with execution result and status
    """
    action_type = approval_data.get('action', 'unknown')

    logger.info(f"Executing action: {action_type} - {approval_data.get('file_path', 'unknown')}")

    try:
        if action_type == 'email_send':
            result = execute_email_send(approval_data)
        elif action_type == 'linkedin_post':
            result = execute_linkedin_post(approval_data)
        elif action_type == 'payment_draft':
            result = execute_payment_draft(approval_data)
        elif action_type == 'social_media_post':
            result = execute_social_media_post(approval_data)
        elif action_type == 'file_share':
            result = execute_file_share(approval_data)
        elif action_type == 'api_call':
            result = execute_api_call(approval_data)
        else:
            result = {
                'status': 'failed',
                'error': f'Unsupported action type: {action_type}',
                'result': None
            }

        # Add execution timestamp
        result['executed_at'] = datetime.now().isoformat()

        logger.info(f"Action execution result: {result['status']} for {action_type}")
        return result

    except Exception as e:
        logger.error(f"Error executing action {action_type}: {e}")
        return {
            'status': 'failed',
            'error': str(e),
            'result': None,
            'executed_at': datetime.now().isoformat()
        }


def execute_email_send(approval_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute email sending action.

    Args:
        approval_data: Approval request data

    Returns:
        Execution result
    """
    # In a real implementation, this would connect to an email service
    # For now, we'll simulate the action
    details = approval_data.get('details', {})

    # Log the intended action (without actually sending email)
    logger.info(f"Would send email to: {details.get('to', 'unknown')}")
    logger.info(f"Subject: {details.get('subject', 'no subject')}")

    # Simulate success
    return {
        'status': 'success',
        'result': f"Email would have been sent to {details.get('to', 'unknown')}",
        'details': {
            'to': details.get('to'),
            'subject': details.get('subject')
        }
    }


def execute_linkedin_post(approval_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute LinkedIn post action.

    Args:
        approval_data: Approval request data

    Returns:
        Execution result
    """
    # In a real implementation, this would connect to LinkedIn API
    details = approval_data.get('details', {})

    logger.info(f"Would post to LinkedIn: {details.get('content_preview', 'no content')[:50]}...")

    # Simulate success
    return {
        'status': 'success',
        'result': "LinkedIn post would have been created",
        'details': {
            'content_preview': details.get('content_preview'),
            'audience': details.get('audience', 'default')
        }
    }


def execute_payment_draft(approval_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute payment draft action.

    Args:
        approval_data: Approval request data

    Returns:
        Execution result
    """
    # In a real implementation, this would connect to a payment service
    details = approval_data.get('details', {})

    logger.info(f"Would draft payment: {details.get('amount', 'unknown')} to {details.get('recipient', 'unknown')}")

    # Simulate success
    return {
        'status': 'success',
        'result': f"Payment of {details.get('amount', 'unknown')} would have been drafted",
        'details': {
            'amount': details.get('amount'),
            'recipient': details.get('recipient'),
            'reason': details.get('reason')
        }
    }


def execute_social_media_post(approval_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute social media post action.

    Args:
        approval_data: Approval request data

    Returns:
        Execution result
    """
    # In a real implementation, this would connect to various social media APIs
    details = approval_data.get('details', {})

    logger.info(f"Would post to {details.get('platform', 'unknown')}: {details.get('content_preview', 'no content')[:50]}...")

    # Simulate success
    return {
        'status': 'success',
        'result': f"Post would have been created on {details.get('platform', 'unknown')}",
        'details': {
            'platform': details.get('platform'),
            'content_preview': details.get('content_preview')
        }
    }


def execute_file_share(approval_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute file sharing action.

    Args:
        approval_data: Approval request data

    Returns:
        Execution result
    """
    # In a real implementation, this would connect to file sharing services
    details = approval_data.get('details', {})

    logger.info(f"Would share file {details.get('file_path', 'unknown')} with {details.get('recipient', 'unknown')}")

    # Simulate success
    return {
        'status': 'success',
        'result': f"File {details.get('file_path', 'unknown')} would have been shared",
        'details': {
            'file_path': details.get('file_path'),
            'recipient': details.get('recipient'),
            'permissions': details.get('permissions', 'read')
        }
    }


def execute_api_call(approval_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute API call action.

    Args:
        approval_data: Approval request data

    Returns:
        Execution result
    """
    # In a real implementation, this would make the actual API call
    details = approval_data.get('details', {})

    logger.info(f"Would make {details.get('method', 'GET')} call to {details.get('endpoint', 'unknown')}")

    # Simulate success
    return {
        'status': 'success',
        'result': f"API call to {details.get('endpoint', 'unknown')} would have been made",
        'details': {
            'endpoint': details.get('endpoint'),
            'method': details.get('method'),
            'payload_preview': details.get('payload_preview')
        }
    }


def log_execution_result(
    approval_data: Dict[str, Any],
    execution_result: Dict[str, Any],
    log_dir: Path
) -> bool:
    """
    Log the execution result to the logs directory.

    Args:
        approval_data: Original approval request data
        execution_result: Result of the execution
        log_dir: Directory to write the log file

    Returns:
        True if successful, False otherwise
    """
    try:
        import uuid
        from utils.file_operations import safe_write_to_file

        # Generate a unique filename for the log
        action_type = approval_data.get('action', 'unknown')
        unique_id = str(uuid.uuid4())

        log_filename = log_dir / f"{action_type}_{unique_id}_processed.md"

        # Create log content
        log_content = f"""---
original_request: "{approval_data.get('file_path', 'unknown')}"
action: "{action_type}"
status: "{execution_result.get('status', 'unknown')}"
executed_at: "{execution_result.get('executed_at', datetime.now().isoformat())}"
executor: "system"
---
# Execution Log: {action_type}

**Original File**: {approval_data.get('file_path', 'unknown')}
**Action Type**: {action_type}
**Status**: {execution_result.get('status', 'unknown')}
**Executed At**: {execution_result.get('executed_at', datetime.now().isoformat())}

## Result Details
{execution_result.get('result', 'No result message')}

## Original Details
```json
{json.dumps(approval_data.get('details', {}), indent=2)}
```

## Execution Info
- **Executor**: system
- **Result Status**: {execution_result.get('status', 'unknown')}
- **Error**: {execution_result.get('error', 'None')}
"""

        # Write the log file
        success = safe_write_to_file(log_filename, log_content)

        if success:
            logger.info(f"Execution result logged to: {log_filename}")
        else:
            logger.error(f"Failed to log execution result to: {log_filename}")

        return success

    except Exception as e:
        logger.error(f"Error logging execution result: {e}")
        return False


# Import json for use in log_execution_result
import json
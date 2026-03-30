"""
File operations utilities for Approval Workflow
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def atomic_move(src: Path, dst: Path) -> bool:
    """
    Atomically move a file from src to dst.

    Args:
        src: Source file path
        dst: Destination file path

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create destination directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)

        # Perform atomic move
        shutil.move(str(src), str(dst))
        logger.debug(f"Atomic move completed: {src} -> {dst}")
        return True
    except Exception as e:
        logger.error(f"Failed to move file {src} to {dst}: {e}")
        return False


def safe_write_to_file(file_path: Path, content: str) -> bool:
    """
    Safely write content to a file using atomic operations.

    Args:
        file_path: Path to write to
        content: Content to write

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to a temporary file first
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=file_path.parent) as tmp_file:
            tmp_file.write(content)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
            temp_path = Path(tmp_file.name)

        # Atomically move the temporary file to the target location
        if atomic_move(temp_path, file_path):
            logger.debug(f"Successfully wrote to file: {file_path}")
            return True
        else:
            # If atomic move failed, clean up the temp file
            try:
                temp_path.unlink()
            except:
                pass  # Ignore cleanup errors
            return False

    except Exception as e:
        logger.error(f"Failed to write to file {file_path}: {e}")
        # Clean up temp file if it exists
        try:
            temp_path.unlink()
        except:
            pass
        return False


def validate_file_path(file_path: Path, allowed_base_dirs: list) -> bool:
    """
    Validate that a file path is within allowed directories to prevent path traversal.

    Args:
        file_path: Path to validate
        allowed_base_dirs: List of allowed base directories

    Returns:
        True if path is valid, False otherwise
    """
    try:
        file_abs = file_path.resolve()
        for base_dir in allowed_base_dirs:
            base_abs = Path(base_dir).resolve()
            if file_abs.is_relative_to(base_abs):
                return True
        return False
    except Exception:
        return False


def file_exists_and_readable(file_path: Path) -> bool:
    """
    Check if a file exists and is readable.

    Args:
        file_path: Path to check

    Returns:
        True if file exists and is readable, False otherwise
    """
    return file_path.exists() and os.access(file_path, os.R_OK)


def get_file_size(file_path: Path) -> Optional[int]:
    """
    Get the size of a file in bytes.

    Args:
        file_path: Path to the file

    Returns:
        Size in bytes or None if file doesn't exist
    """
    if file_path.exists():
        return file_path.stat().st_size
    return None
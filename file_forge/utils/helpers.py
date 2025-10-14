"""
Utility helper functions
"""

from pathlib import Path
from typing import List


def get_file_size_readable(file_path: Path) -> str:
    """
    Get human-readable file size

    Args:
        file_path: Path to file

    Returns:
        Human-readable file size string
    """
    size_bytes = float(file_path.stat().st_size)

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.2f} PB"


def validate_file_exists(file_path: Path) -> bool:
    """
    Validate that a file exists

    Args:
        file_path: Path to file

    Returns:
        True if file exists, raises FileNotFoundError otherwise
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    return True


def get_supported_image_formats() -> List[str]:
    """Get list of supported image formats"""
    return ["jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff", "ico"]


def get_supported_document_formats() -> List[str]:
    """Get list of supported document formats"""
    return []

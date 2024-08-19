"""
Sonarr Backup Type Enum
"""

from enum import Enum


class BackupType(Enum):
    """
    Backup Type
    """
    SCHEDULED = "scheduled"
    MANUAL = "manual"
    UPDATE = "update"

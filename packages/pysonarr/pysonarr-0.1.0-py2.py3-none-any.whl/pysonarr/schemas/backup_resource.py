"""
Backup Resource Schema
"""

from typing import Optional

from pydantic import BaseModel

from src.pysonarr.enums.backup_resource import BackupType


class BackupResource(BaseModel):
    """
    Backup Resource
    """
    id: int
    name: Optional[str]
    path: Optional[str]
    type_: BackupType
    size: int
    time: str

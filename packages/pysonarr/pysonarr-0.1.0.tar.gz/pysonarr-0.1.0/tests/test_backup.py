"""
Tests for the Backup class.
"""

from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv

from src.pysonarr.backup import Backup
from src.pysonarr.client import SonarrClient
from src.pysonarr.schemas.backup_resource import BackupResource

load_dotenv()


@pytest.fixture
def mock_client():
    """
    Mock SonarrClient
    """
    mock_base_url = "http://localhost:8989"
    mock_api_key = "mock_api_key"

    return SonarrClient(
        base_url=MagicMock(mock_base_url),
        api_key=MagicMock(mock_api_key)
    )


def test_get_backups(mock_client: SonarrClient):
    """
    Test Backup.get()
    """
    # Mock the Backup.get method to return a list of BackupResource instances
    mock_backup_resource = MagicMock(spec=BackupResource)
    mock_client.get = MagicMock(
        return_value=[mock_backup_resource, mock_backup_resource])

    backup = Backup(mock_client)
    backups = backup.get()
    assert isinstance(backups, list)
    assert all(isinstance(b, BackupResource) for b in backups)


def test_delete_backup_by_id(mock_client: SonarrClient):
    """
    Test Backup.delete_by_id()
    """
    # Mock the Backup.delete_by_id method to return True
    mock_client.delete = MagicMock(return_value=True)

    backup = Backup(mock_client)
    assert backup.delete_by_id(1) is True


def test_restore_backup_by_id(mock_client: SonarrClient):
    """
    Test Backup.restore_by_id()
    """
    # Mock the Backup.restore_by_id method to return True
    mock_client.post = MagicMock(return_value=True)

    backup = Backup(mock_client)
    assert backup.restore_by_id(1) is True


def test_restore_backup_with_upload(mock_client: SonarrClient):
    """
    Test Backup.restore_with_upload()
    """
    # Mock the Backup.restore_by_id method to return True
    mock_client.post = MagicMock(return_value=True)

    backup = Backup(mock_client)
    assert backup.restore_with_upload() is True

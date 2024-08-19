"""
Sonarr Backup Module
"""

from src.pysonarr.client import SonarrClient
from src.pysonarr.schemas.backup_resource import BackupResource


class Backup:
    """
    Backup class
    """

    def __init__(self, client: SonarrClient):
        """
        Backup constructor

        :param client: SonarrClient
        """
        self.client = client

    def get(self) -> list[BackupResource]:
        """
        Get all backups

        :return: List of BackupResource
        """

        return self.client.get(endpoint="/api/v3/system/backup", params=None)

    def delete_by_id(self, backup_id: int) -> bool:
        """
        Delete a backup by ID

        :param backup_id: Backup ID

        :return: True if successful
        """
        if not backup_id:
            raise ValueError("backup_id is required")

        delete_response = self.client.delete(
            endpoint=f"/api/v3/system/backup/{backup_id}"
        )

        return delete_response

    def restore_by_id(self, backup_id: int) -> bool:
        """
        Restore a backup by ID

        :param backup_id: Backup ID

        :return: True if successful
        """
        if not backup_id:
            raise ValueError("backup_id is required")

        restore_by_id_response = self.client.post(
            endpoint=f"/api/v3/system/backup/restore/{backup_id}"
        )

        return restore_by_id_response

    def restore_with_upload(self) -> bool:
        """
        Restore with upload

        :return: True if successful
        """
        restore_with_upload_response = self.client.post(
            endpoint="/api/v3/system/backup/restore/upload"
        )

        return restore_with_upload_response

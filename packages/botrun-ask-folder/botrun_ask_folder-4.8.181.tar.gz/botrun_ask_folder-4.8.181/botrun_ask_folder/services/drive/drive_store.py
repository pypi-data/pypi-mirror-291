from abc import ABC, abstractmethod

from botrun_ask_folder.models.drive_folder import DriveFolder
from botrun_ask_folder.models.drive_file import DriveFile
from botrun_ask_folder.models.splitted_file import SplittedFile

DRIVE_FOLDER_STORE_NAME = "drive-folder-store"
DRIVE_FILE_STORE_NAME = "drive-file-store"
SPLITTED_FILE_STORE_NAME = "splitted-file-store"


class DriveFolderStore(ABC):
    @abstractmethod
    async def get_drive_folder(self, item_id: str) -> DriveFolder:
        pass

    @abstractmethod
    async def set_drive_folder(self, item: DriveFolder):
        pass

    @abstractmethod
    async def delete_drive_folder(self, item_id: str):
        pass

    @staticmethod
    def get_drive_folder_store_key(item_id: str) -> str:
        return f"{DRIVE_FOLDER_STORE_NAME}:{item_id}"


class DriveFileStore(ABC):
    @abstractmethod
    async def get_drive_file(self, file_id: str) -> DriveFile:
        pass

    @abstractmethod
    async def set_drive_file(self, file: DriveFile):
        pass

    @abstractmethod
    async def delete_drive_file(self, file_id: str):
        pass

    @staticmethod
    def get_drive_file_store_key(file_id: str) -> str:
        return f"{DRIVE_FILE_STORE_NAME}:{file_id}"


class SplittedFileStore(ABC):
    @abstractmethod
    async def get_splitted_file(self, splitted_file_id: str) -> SplittedFile:
        pass

    @abstractmethod
    async def set_splitted_file(self, file: SplittedFile):
        pass

    @abstractmethod
    async def delete_splitted_file(self, splitted_file_id: str):
        pass

    @staticmethod
    def get_splitted_file_store_key(splitted_file_id: str) -> str:
        return f"{SPLITTED_FILE_STORE_NAME}:{splitted_file_id}"

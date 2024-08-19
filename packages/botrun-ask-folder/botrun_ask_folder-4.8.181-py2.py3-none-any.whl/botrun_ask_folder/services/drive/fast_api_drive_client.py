import aiohttp
import os
from typing import List

from botrun_ask_folder.models.drive_folder import DriveFolder
from botrun_ask_folder.models.drive_file import DriveFile
from botrun_ask_folder.models.splitted_file import SplittedFile
from botrun_ask_folder.services.drive.drive_client import DriveClient

API_PREFIX = "api/botrun/botrun_ask_folder"


class FastAPIDriveClient(DriveClient):
    def __init__(self, api_url: str = os.getenv("FAST_API_URL")):
        self.api_url = api_url

    async def get_drive_folder(self, id: str) -> DriveFolder:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/{API_PREFIX}/drive_folder/{id}"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return DriveFolder(**data)

    async def set_drive_folder(self, folder: DriveFolder) -> DriveFolder:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/{API_PREFIX}/drive_folder", json=folder.model_dump()
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return DriveFolder(**data["drive_folder"])

    async def delete_drive_folder(self, id: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.api_url}/{API_PREFIX}/drive_folder/{id}"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data["message"] == "Status deleted successfully"

    async def get_drive_file(self, id: str) -> DriveFile:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/{API_PREFIX}/drive_file/{id}"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return DriveFile(**data)

    async def set_drive_file(self, file: DriveFile) -> DriveFile:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/{API_PREFIX}/drive_file", json=file.model_dump()
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return DriveFile(**data["drive_file"])

    async def delete_drive_file(self, id: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.api_url}/{API_PREFIX}/drive_file/{id}"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data["message"] == "File deleted successfully"

    async def get_splitted_file(self, id: str) -> SplittedFile:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/{API_PREFIX}/splitted_file/{id}"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return SplittedFile(**data)

    async def set_splitted_file(self, file: SplittedFile) -> SplittedFile:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/{API_PREFIX}/splitted_file", json=file.model_dump()
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return SplittedFile(**data["splitted_file"])

    async def delete_splitted_file(self, id: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.api_url}/{API_PREFIX}/splitted_file/{id}"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data["message"] == "Splitted file deleted successfully"

    async def update_drive_files(self, folder_id: str, new_files: List[DriveFile]):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/{API_PREFIX}/drive_folder/{folder_id}/update_files",
                json=[file.model_dump() for file in new_files],
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data

    async def get_split_files(self, folder_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/{API_PREFIX}/drive_folder/{folder_id}/split_files"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return {
                    name: SplittedFile(**file_data) for name, file_data in data.items()
                }

    async def get_drive_files(self, folder_id: str) -> List[DriveFile]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/{API_PREFIX}/drive_folder/{folder_id}/files"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return [DriveFile(**file_data) for file_data in data]

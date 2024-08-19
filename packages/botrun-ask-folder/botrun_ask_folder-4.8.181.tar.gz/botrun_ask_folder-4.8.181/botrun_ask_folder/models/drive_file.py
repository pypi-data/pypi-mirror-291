from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .splitted_file import SplittedFile


class DriveFile(BaseModel):
    """
    Represents an item in a collection, typically a file or folder.

    Attributes:
        id (str): Google file id
        name (str): 檔案名字，如果是處理過後的檔案，會存split過後的檔名
        mimeType (str): MIME type of the item.
        modifiedTime (str): Last modification time of the item.
        size (str): Size of the item, typically in bytes.
        parent (str): 在 Google Drive 上的 parent
        path (str): 在 Google Drive 上的 parent Full path
        splitted_files (List[str]): List of SplittedFile ids
    """

    id: str
    name: str
    mimeType: str
    modifiedTime: str
    size: str
    parent: str
    path: str
    splitted_files: List[str] = []

    @classmethod
    def from_json(cls, json_str: str) -> "DriveFile":
        return cls.model_validate_json(json_str)

    def to_json(self) -> str:
        return self.model_dump_json(exclude_none=True)

    @classmethod
    def from_list(cls, item_list: List[dict]) -> List["DriveFile"]:
        return [cls(**item) for item in item_list]

    @classmethod
    def to_list(cls, items: List["DriveFile"]) -> List[dict]:
        return [item.model_dump(exclude_none=True) for item in items]

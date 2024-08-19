from pydantic import BaseModel, Field
from typing import List, Dict
from enum import Enum
from .drive_file import DriveFile
from .splitted_file import SplittedFile


class FolderStatusEnum(str, Enum):
    """
    Enumeration of possible collection statuses.
    """

    PROCESSING = "PROCESSING"
    DONE = "DONE"


class DriveFolder(BaseModel):
    """
    Represents the status of a collection.也就是 Google Drive 的一個 folder

    Attributes:
        id (str): Unique identifier for the collection.
        status (CollectionStatusEnum): Current status of the collection.
        items (List[str]): List of DriveFile ids in the collection.
    """

    id: str = Field(..., description="Unique identifier for the collection")
    status: FolderStatusEnum = Field(
        ..., description="Current status of the collection"
    )
    items: List[str] = Field(
        default_factory=list, description="List of DriveFile ids in the collection"
    )

    @classmethod
    def model_validate_json(cls, json_data: str) -> "DriveFolder":
        """
        Create a CollectionStatus instance from a JSON string.

        Args:
            json_data (str): JSON string representing a CollectionStatus.

        Returns:
            CollectionStatus: An instance of CollectionStatus.
        """
        return super().model_validate_json(json_data)

    def model_dump_json(self, **kwargs) -> str:
        """
        Convert the CollectionStatus instance to a JSON string.

        Returns:
            str: JSON representation of the CollectionStatus.
        """
        return super().model_dump_json(**kwargs)

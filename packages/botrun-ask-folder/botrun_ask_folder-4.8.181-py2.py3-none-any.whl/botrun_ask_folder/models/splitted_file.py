from pydantic import BaseModel
from typing import Optional


class SplittedFile(BaseModel):
    """
    Represents a split item from a collection item.

    Attributes:
        id (str): Unique identifier for the split item
        name (str): Name of the split item
        gen_page_imgs (bool): Whether page images have been generated for this item
        ori_file_name (str): Original file name this item was split from
        modified_time (str): Modified time of this split item
        page_number (Optional[int]): Page number of this split item
        sheet_name (Optional[str]): Sheet name of this split item
        file_id (str): ID of the DriveFile this split file belongs to
    """

    id: str
    name: str
    gen_page_imgs: bool = False
    ori_file_name: str
    modified_time: str
    page_number: Optional[int] = None
    sheet_name: Optional[str] = None
    file_id: str

    @classmethod
    def from_json(cls, json_str: str) -> "SplittedFile":
        return cls.model_validate_json(json_str)

    def to_json(self) -> str:
        return self.model_dump_json(exclude_none=True)

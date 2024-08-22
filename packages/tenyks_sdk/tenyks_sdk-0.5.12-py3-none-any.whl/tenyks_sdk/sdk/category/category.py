import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Category(BaseModel):
    name: str = Field(
        description="Name of the category",
        examples=["cat", "dog", "car"],
    )
    color: Optional[str] = Field(
        description="Hex color code of the category (the bounding box color).",
        examples=["#FF0000", "#00FF00", "#0000FF"],
        default="#000000",
    )
    id: Optional[int] = Field(
        description="Unique dataset category ID, the index of the category in the dataset categories list",
        examples=[0, 1, 2],
        ge=0,
        default=None,
    )

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v):
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", v):
            raise ValueError("Invalid hex color")
        return v

from datetime import datetime
from typing import Any, ClassVar, Dict

from pydantic import BaseModel


class ParsedLogEntry(BaseModel):
    version: int
    parsed_fields: Dict[str, Any]

    class Config:
        arbitrary_types_allowed: ClassVar[bool] = True
        json_encoders: ClassVar[Dict[type, Any]] = {
            datetime: lambda v: v.isoformat(),
        }

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class ParsedLogEntry(BaseModel):
    version: int
    parsed_fields: Dict[str, Any]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        },
    )

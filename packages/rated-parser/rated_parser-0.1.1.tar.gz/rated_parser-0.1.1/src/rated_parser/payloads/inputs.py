from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, field_validator


class FieldType(str, Enum):
    TIMESTAMP = "timestamp"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"


class LogFormat(str, Enum):
    RAW_TEXT = "raw_text"
    JSON = "json_dict"


class FieldDefinition(BaseModel):
    key: str
    field_type: FieldType
    format: Optional[str] = None

    @field_validator("format")
    def validate_format(cls, v, info):  # noqa
        field_type = info.data.get("field_type")
        if field_type == FieldType.TIMESTAMP and not v:
            raise ValueError("Format is required for timestamp fields")
        return v


class RawTextFieldDefinition(FieldDefinition):
    value: str


class JsonFieldDefinition(FieldDefinition):
    path: str


class LogPatternPayload(BaseModel):
    version: int
    log_format: LogFormat


class RawTextLogPatternPayload(LogPatternPayload):
    log_example: str
    fields: List[RawTextFieldDefinition]


class JsonLogPatternPayload(LogPatternPayload):
    fields: List[JsonFieldDefinition]

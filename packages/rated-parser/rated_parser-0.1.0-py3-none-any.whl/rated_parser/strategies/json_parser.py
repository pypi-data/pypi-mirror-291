from typing import Any, Dict, List, Mapping

from ..exceptions import ParserError
from ..payloads.inputs import JsonFieldDefinition
from .base import ParserStrategy


class JsonParserStrategy(ParserStrategy[JsonFieldDefinition]):
    def parse(
        self, log: Dict[str, Any], fields: Mapping[str, JsonFieldDefinition]
    ) -> Dict[str, Any]:
        if not isinstance(log, dict):
            raise ParserError(
                "JsonParserStrategy requires a dictionary or a valid JSON string"
            )

        matched_fields = {}
        for key, field_def in fields.items():
            if isinstance(field_def, JsonFieldDefinition):
                value = self._get_nested_value(log, field_def.path.split("."))
                if value is not None:
                    matched_fields[key] = value

        return self._convert_types(matched_fields, fields)

    @staticmethod
    def _get_nested_value(data: Dict[str, Any], keys: List[str]) -> Any:
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

from typing import Any, Dict

from pygrok import Grok  # type: ignore

from ..exceptions import ParserError
from ..payloads.inputs import RawTextFieldDefinition
from .base import ParserStrategy


class GrokParserStrategy(ParserStrategy[RawTextFieldDefinition]):
    def __init__(self, pattern: str):
        self.grok = Grok(pattern)

    def parse(
        self, log: str, fields: Dict[str, RawTextFieldDefinition]
    ) -> Dict[str, Any]:
        match = self.grok.match(log)
        if not match:
            raise ParserError("Failed to parse log with the given pattern")
        return self._convert_types(match, fields)

from typing import Any, Dict, Union

from ..exceptions import ParserError, PatternError
from ..payloads.inputs import JsonLogPatternPayload, LogFormat, RawTextLogPatternPayload
from ..payloads.types import ParsedLogEntry
from ..utils.factory import create_parser


class LogParser:
    def __init__(self):
        """
        Initializes the log parser with an empty dictionary of patterns
        """
        self.patterns: Dict[int, Dict[str, Any]] = {}

    def add_pattern(self, pattern_dict: Dict[str, Any]) -> None:
        """
        Accepts dictionary for both: RawTextLogPatternPayload, JsonLogPatternPayload
        """
        pattern: Union[RawTextLogPatternPayload, JsonLogPatternPayload]
        log_format_str = pattern_dict["log_format"].lower()

        try:
            if log_format_str == LogFormat.RAW_TEXT:
                pattern = RawTextLogPatternPayload(**pattern_dict)
            elif log_format_str == LogFormat.JSON:
                pattern = JsonLogPatternPayload(**pattern_dict)
            else:
                raise PatternError(
                    f"Invalid log format {log_format_str}, "
                    f"use 'raw_text' or 'json_dict'"
                )

            if pattern.version in self.patterns:
                raise PatternError(f"Pattern version {pattern.version} already exists")

            parser = create_parser(pattern)
            self.patterns[pattern.version] = {
                "parser": parser,
                "fields": {field.key: field for field in pattern.fields},
            }
        except Exception as e:
            raise PatternError(f"Error adding pattern: {e!s}")

    def parse_log(
        self, log: Union[str, Dict[str, Any]], version: int
    ) -> ParsedLogEntry:
        if version not in self.patterns:
            raise ParserError(f"Unknown pattern version: {version}")

        pattern = self.patterns[version]
        parser = pattern["parser"]
        fields = pattern["fields"]

        try:
            parsed_fields = parser.parse(log, fields)
            return ParsedLogEntry(version=version, parsed_fields=parsed_fields)
        except Exception as e:
            raise ParserError(f"Error parsing log: {e!s}")

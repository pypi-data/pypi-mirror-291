from typing import Any

import json_repair
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.outputs import Generation


class RepairableJsonOutputParser(JsonOutputParser):

    def parse(self, text: str) -> Any:
        repaired_text = json_repair.repair_json(text)
        if repaired_text == "\"\"" or repaired_text == "{}":
            return self.parse_result([Generation(text=text)])
        return self.parse_result([Generation(text=repaired_text)])


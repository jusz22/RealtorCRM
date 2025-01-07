from dataclasses import dataclass
from typing import Any

from app.infrastructure.const import OPERATORS


@dataclass()
class FilterDTO:
    field: str | None
    operator: str | None
    value: Any | None


    def get_operator(self):
        operator = OPERATORS[self.operator]
        return operator


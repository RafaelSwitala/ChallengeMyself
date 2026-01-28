from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Field:
    name: str
    type: str
    unit: Optional[str] = None
    values: Optional[List[str]] = None

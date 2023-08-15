from dataclasses import dataclass
from processing.models.Literal import Literal

@dataclass
class Clause:
    literals: list[Literal]
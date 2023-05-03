from dataclasses import dataclass
from models.Literal import Literal

@dataclass
class Clause:
    literals: list[Literal]
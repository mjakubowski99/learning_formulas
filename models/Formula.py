from dataclasses import dataclass
from models.Clause import Clause

@dataclass
class Formula:
    cluases: list[Clause]
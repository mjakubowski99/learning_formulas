from dataclasses import dataclass

@dataclass
class Treshold:
    fill_na_treshold: float
    drop_na_treshold: float

    def __post_init__(self):
        if self.drop_na_treshold < self.fill_na_treshold:
            raise Exception("Fill treshold must be greater than drop_na treshold")
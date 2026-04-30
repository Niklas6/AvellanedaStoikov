



from dataclasses import dataclass











@dataclass
class SimParams:
    S0: float = 100
    sigma: float = 2

    money: float = 1000
    q: int = 0

    T: float = 1.0
    m: int = 200
    gamma: float = 0.1

    A: float = 140
    k: float = 1.5

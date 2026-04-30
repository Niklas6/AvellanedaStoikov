
import numpy as np

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.config import SimParams





@dataclass
class MarketState:
    t: float
    step: int
    price: float
    cash: float
    inventory: int
    SP: SimParams


class TradingAgent(ABC):
    @abstractmethod
    def quote(self, state: MarketState) -> tuple[float, float]:
        """Return bid_delta, ask_delta."""
        pass



@dataclass
class ConstantSpreadAgent(TradingAgent):
    bid_delta: float = 1.0
    ask_delta: float = 1.0

    def quote(self, state: MarketState) -> tuple[float, float]:
        return self.bid_delta, self.ask_delta


@dataclass
class SymmetricAgent(TradingAgent):

    def quote(self, state: MarketState) -> tuple[float, float]:
        #SP = state.SP
        r = state.SP.gamma * state.SP.sigma ** 2 * (state.SP.T - state.t) + 2 * np.log(1 + state.SP.gamma / state.SP.k) / state.SP.gamma

        return r/2,r/2

@dataclass
class ASModelAgent(TradingAgent):

    def quote(self, state: MarketState) -> tuple[float, float]:
        r = state.SP.gamma * state.SP.sigma ** 2 * (state.SP.T - state.t) + 2 * np.log(1 + state.SP.gamma / state.SP.k) / state.SP.gamma
        skew=state.inventory*state.SP.gamma*state.SP.sigma**2*(state.SP.T - state.t)/state.SP.T
        #print(r,skew,state.inventory,state.SP.T, state.t)

        return r/2+skew,r/2-skew


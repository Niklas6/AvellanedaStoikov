#from tensorflow import keras
#from tensorflow.keras import layers
from dataclasses import dataclass

from src.config import SimParams
from src import stochastic_processes
from src.simulator import simulation
from src.market_makers import TradingAgent


'''
The neuronal network should train with timesteps and give a 'TradingAgent' which maps 
MarketState -> bid_delta, ask_delta

class MarketState:
    t: float
    step: int
    price: float
    cash: float
    inventory: int
    SP: SimParams

Train data: MarketStates
predict: bid_delta, ask_delta
revenue
'''
@dataclass
class NeuralNetworkAgent(TradingAgent):
    bid_delta: float = 1.0
    ask_delta: float = 1.0

    def quote(self, state: MarketState) -> tuple[float, float]:
        return self.bid_delta, self.ask_delta



def model_trainer(SP: SimParams,ntrain: int=100):
    NN=NeuralNetworkAgent()

    for i in range(100):
        Processes = stochastic_processes.get_stochastic_processes(SP)
        St = Processes['stock']
        Buy_a = Processes['asks']
        Buy_b = Processes['bids']
        sim = simulation(SP,St,Buy_a,Buy_b, NN)
        Eval = sim['TotalValue'][-1]-SP.money
        print(Eval)

    #return(NeuralNetworkAgent)

model_trainer(SimParams(),10 )

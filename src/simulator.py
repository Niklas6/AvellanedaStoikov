import numpy as np





from src import stochastic_processes
from src.market_makers import MarketState, TradingAgent
from src.config import SimParams

import matplotlib.pyplot as plt










#print(stochastic_processes.buys(200))


def simulation(SP: SimParams,St,Buy_a,Buy_b, agent: TradingAgent):
    dmoney=[SP.money]
    dq=[SP.q]
    money=SP.money
    Money=[money]
    inventory=SP.q
    Inventory = [inventory]

    for i in range(SP.m-1):
        state =MarketState(t=i*SP.T/SP.m,
                           step=i,
                           price=St[i],
                           cash=Money[i],
                           inventory=Inventory[i],
                           SP=SP)

        db, da = agent.quote(state)

        asks_filled = stochastic_processes.get_ask( stochastic_processes.lambda_intensity(SP.A,SP.k,da), Buy_a[i],inventory+10)
        bids_filled = stochastic_processes.get_bid( stochastic_processes.lambda_intensity(SP.A,SP.k,db), Buy_b[i],money/St[i])


        money+=asks_filled*(St[i]+da) + bids_filled*(db-St[i])
        inventory+=bids_filled-asks_filled

        Money+= [money]
        Inventory+=[inventory]
    Money = np.array(Money)
    Inventory= np.array(Inventory)

    TotalValue=Money+Inventory*St
    value_function=-np.exp(-SP.gamma*(TotalValue-TotalValue[0]))

    return {
        'q_stocks': Inventory,
        'money': Money,
        'TotalValue': TotalValue,
        'value_function': value_function
    }

'''SP=SimParams()



result =simulation(SP,
                stochastic_processes.BM_stock(SP.S0, SP.m, SP.T, 0, SP.sigma),
                stochastic_processes.buys(SP.m),
                stochastic_processes.buys(SP.m)

                  )
fig, axis = plt.subplots(2,3,figsize=(20,10))
axis[0,0].plot(result['q_stocks'])
axis[0,1].plot(result['money'])
axis[0,2].plot(result['TotalValue'])



plt.show()
'''





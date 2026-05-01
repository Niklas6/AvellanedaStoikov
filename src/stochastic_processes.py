import numpy as np






def get_stochastic_processes(SP):
    jumps=[np.zeros(SP.m),np.zeros(SP.m)]

    if SP.market_condition == 'fair':
        St = df_fair_experiment(SP)
        Buy_a = buys(SP)
        Buy_b = buys(SP)



    if SP.market_condition == 'insider':
        jumps = event_jumps(SP)

        St = df_fair_experiment(SP)+ np.cumsum(jumps[2])
        Buy_a = buys(SP)
        Buy_b = buys(SP)
        for i in range(SP.m-1):
            #print(jumps[0][i+1])
            if jumps[0][i+1]>0:
                Buy_a[i]=np.concatenate(([0,0,0,0,0],Buy_a[i][0:5]))

            if jumps[1][i+1]>0:
                Buy_b[i]=np.concatenate(([0,0,0,0,0],Buy_b[i][0:5]))
                #print(np.concatenate(([0,0,0,0,0],Buy_a[i][0:5])))





    return {
        'stock': St,
        'asks':Buy_a,
        'bids':Buy_b,
        'jumps':jumps
    }








'''This function models a stock using a drifted Brownian motion '''
def df_fair_experiment(SP):
    dstock=np.random.normal(0, SP.sigma / np.sqrt(SP.m), SP.m)
    return(SP.S0+np.cumsum(dstock))

def event_jumps(SP):
    jump_down =np.random.poisson(1/2/SP.m/SP.T,SP.m)
    jump_up =np.random.poisson(1/2/SP.m/SP.T,SP.m)
    jump_up_down = jump_up-jump_down
    jump = jump_up_down* np.random.normal(2, 2, SP.m)

    return  [jump_up, jump_down, jump]




'''This function gives a for each time step an array of maximal prices to recive a order'''
def buys(SP,ordermax=10):
    rexp=[]
    if SP.market_condition == 'fair':
        for i in range(SP.m):
            rexp += [np.cumsum(np.random.exponential(SP.m/SP.T, ordermax))]

    if SP.market_condition == 'insider':
        for i in range(SP.m):
            rexp += [np.cumsum(np.random.exponential(SP.m/SP.T, ordermax))]
    return rexp




'''This function gives for a given lambda and timestamp the amount of orders recived'''
def get_ask(lam,rexp,max_ask):

    for j in range(10):
        if rexp[j]>lam:
            return min(j,max_ask)
    return min(10,max_ask)


def get_bid(lam,rexp,max_bid):
    for j in range(10):
        if rexp[j]>lam:
            return min(j,max_bid)
    return min(10,max_bid)


def lambda_intensity(A,k,delta):
    return A*np.exp(-k*delta)

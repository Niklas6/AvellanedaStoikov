import numpy as np


'''This function models a stock using a drifted Brownian motion '''
def BM_stock(S0, m,T,mu,sigma):
    dstock=np.random.normal(mu, sigma / np.sqrt(m), m)
    return(S0+np.cumsum(dstock))






'''This function gives a for each time step an array of maximal prices to recive a order'''
def buys(T,m,ordermax=10):
    rexp=[]
    for i in range(m):
        rexp += [np.cumsum(np.random.exponential(m/T, ordermax))]
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


from src.config import SimParams
from src import stochastic_processes
from src.simulator import simulation
from src.market_makers import ConstantSpreadAgent, SymmetricAgent, ASModelAgent

import pandas as pd

import numpy as np


from matplotlib.backends.backend_pdf import PdfPages


import matplotlib.pyplot as plt


from IPython.display import display, HTML
from tabulate import tabulate
import argparse

def run_experiments(N,agents,SP):

    #model_names = [name for name in agents.keys()]
    rows=[]
    for sim_id in range(N):
        # SP.market_condition=='fair':
        Processes= stochastic_processes.get_stochastic_processes(SP)
        St = Processes['stock']
        Buy_a = Processes['asks']
        Buy_b = Processes['bids']



        for name, agent in agents.items():
            sim = simulation(SP, St, Buy_a, Buy_b, agent)
            rows.append({
                'simulation_id': sim_id,
                'agent': name,
                'profit': sim['TotalValue'][-1]-SP.money ,
                'average_liquidity': sim['money'].mean(),
                'deviation_liquidity': sim['money'].std()  }
            )
    df=pd.DataFrame(rows)
    #print(df)
    dg=df.groupby('agent', sort=False).agg(
        mean_profit = ('profit',"mean"),
        std_profit =  ('profit',"std"),
        sharpe_profit = ('profit',lambda x: x.mean() / x.std()),
        mean_liquidity = ('average_liquidity',"mean"),
        std_liquidity = ('deviation_liquidity',"std")
    )
        #min= "min",
        #max="max")
    dg=round(dg,2)
    return(dg)


def create_figure(params: SimParams,agents):
    Processes = stochastic_processes.get_stochastic_processes(params)
    prices = Processes['stock']
    ask_orders = Processes['asks']
    bid_orders = Processes['bids']
    #i=0
    fig, axis = plt.subplots(1, 4, figsize=(12, 2.5))
    axis[0].plot(prices, color="black")
    axis[0].set_title("Stock Price")
    #axis[0].set_ylabel("Stock Price")
    axis[0].set_xlabel("time")


    for name, agent in agents.items():
        result = simulation(params, prices, ask_orders, bid_orders, agent)



        axis[1].plot(result['q_stocks'], label=name)
        axis[1].set_title("Inventory")
        axis[1].set_xlabel("time")

        axis[2].plot(result['money'], label=name)
        axis[2].set_title('liquidity')
        axis[2].set_xlabel("time")

        axis[3].plot(result['TotalValue']-params.money, label=name)
        axis[3].set_title("revenue")
        axis[3].set_xlabel("time")
    handles, labels = axis[1].get_legend_handles_labels()

    fig.legend(handles=handles,
               labels=labels,
            loc="center right",
            bbox_to_anchor=(1.08, 0.5),
            title="Agents",
        )


    return fig, axis

def make_dataframe_table_page(nsim,df, title="", max_rows=15):
    preview_df = df.head(max_rows).reset_index()
    preview_df.columns = [col.replace("_", " ").title() for col in preview_df.columns]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.patch.set_facecolor("#f7f8fa")
    ax.set_facecolor("#f7f8fa")
    ax.axis("off")

    ax.text(
        0.5,
        0.93,
        title,
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color="#17202a",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.875,
        "Summary of " + str(nsim) + " Monte Carlo simulations",
        ha="center",
        va="center",
        fontsize=11,
        color="#566573",
        transform=ax.transAxes,
    )

    table = ax.table(
        cellText=preview_df.values,
        colLabels=preview_df.columns,
        loc="center",
        cellLoc="center",
        bbox=[0.08, 0.28, 0.84, 0.46],
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.6)

    header_color = "#263238"
    row_colors = ["#ffffff", "#edf2f7"]
    edge_color = "#d5d8dc"

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(edge_color)
        cell.set_linewidth(0.8)

        if row == 0:
            cell.set_facecolor(header_color)
            cell.get_text().set_color("white")
            cell.get_text().set_fontweight("bold")
        else:
            cell.set_facecolor(row_colors[(row - 1) % 2])
            if col == 0:
                cell.get_text().set_fontweight("bold")
                cell.get_text().set_color("#1f618d")
            else:
                cell.get_text().set_color("#17202a")
    return fig


def parser():
    parser = argparse.ArgumentParser(description="Input for experiments")
    parser.add_argument('--seed', type = int, default = None, help ='Random seed for reproducibility')
    parser.add_argument('--nsims', type = int, default = 1000, help ='Number of simulations')
    return parser.parse_args()


def main():
    parse=parser()
    #print(parse)
    #print(parse.nsims)

    if parse.seed is not None:
        np.random.seed(parse.seed)



    params = SimParams(T=1,m=200)

    agents = {
        "constant": ConstantSpreadAgent(1.0, 1.0),

        "symmetric": SymmetricAgent(),

        "AS Inventory": ASModelAgent(),
    }

    '''we simulate 1000 branches'''
    df_fair_experiment=run_experiments(parse.nsims, agents,params)
    #print(tabulate(dg, headers="keys", tablefmt="github", showindex=True))
    #print(dg)



    df_fair_experiment.to_csv("data_simulation_results/fair_experiment.csv", index=True)

    #params_insider=copy.copy(params)
    #params_insider.market_condition = 'insider'
    #df_insider_experiment=run_experiments(parse.nsims, agents,params_insider)

    #df_insider_experiment.to_csv("experiment_results/insider_experiment.csv", index=True)



    '''we run one example branch'''


    fig, axis=create_figure(params,agents)
    #fig2, axis2=create_figure(params_insider,agents)
        
        
        
        
    plt.savefig("data_simulation_results/fair_examplepath.png", dpi=300)


    with PdfPages("simulation_results.pdf") as pdf:
        pdf.savefig(make_dataframe_table_page(parse.nsims,df_fair_experiment, title="Agent Performance"), bbox_inches="tight")
        pdf.savefig(fig, bbox_inches="tight")
        #pdf.savefig(make_dataframe_table_page(df_insider_experiment, title="Agent Performance in Market with Insider Trader"), bbox_inches="tight")
        #pdf.savefig(fig2, bbox_inches="tight")


if __name__ == "__main__":
    main()

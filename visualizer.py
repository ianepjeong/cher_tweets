import plotly.offline as py
import plotly.graph_objects as go
import networkx as nx
import pandas as pd

from preprocess import process_string_data
from network import network_dict
from markov import Markov
from network import make_network_graph

# function to make a bar graph
def make_bar_graph(df):
    fig2 = go.Figure(
        layout=dict(
        title='Capitalization Pattern', 
        width=1200, height=700, title_x=0.5,
        paper_bgcolor='#fff',
        plot_bgcolor="#fff",
        xaxis=dict(
            title='Next Word', 
            type='category', 
            gridcolor='rgb(255,255,255)',
            zeroline= False,
        ),
        yaxis=dict(
            title='Probility',
            zeroline= False
                )
            )
        )

    # Add the bars
    for row in df.iterrows():
        fig2.add_trace(
            go.Bar(
            x = df.columns,
            y = row[1],
            name = row[0])
            )
    
    # Save the graph
    py.plot(fig2, filename='bars.html')

def go_bar(tweets):
    cases = process_string_data(tweets['text'], True)
    model = Markov(cases)
    df = pd.DataFrame(model.prob_model).T
    make_bar_graph(df)

# make network graph
def go_network(tweets):
    processed = process_string_data(tweets['text'], False)
    make_network_graph(processed)        


if __name__ == '__main__':
    tweets = pd.read_csv('tweets.csv')
    tweets = tweets[:10]
    go_bar(tweets)
    go_network(tweets)

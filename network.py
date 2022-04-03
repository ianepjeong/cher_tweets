import plotly.offline as py
import plotly.graph_objects as go
import networkx as nx

'''
Map a word to its next words.
'''

def network_dict(train_set):
    '''
    For each word in our training data, find every word that follows
    the word and the count for the trailing word.
    
    Input:
    train_set: list of lists of strings
    
    Returns: dictionary of dictionaries
    '''
    network = {}
    
    for lst in train_set:
        for i, word in enumerate(lst):
            network[word] = network.get(word, {})
            if len(lst) - i > 1:
                next_word = lst[i + 1]
                network[word][next_word] = network[word].get(next_word, 0) + 1
    return network

def make_network_graph(words):
    dct = network_dict(words)
    next_word = nx.Graph()

    # initialize nodes
    for word in dct.keys():
        if dct[word]:
            next_word.add_node(word, size = len(dct[word]))
    
    # initialize edges
    for key, val in dct.items():
        for nxt, count in val.items():
            next_word.add_edge(key, nxt, weight = count)
    
    positions = nx.kamada_kawai_layout(next_word)

    # set nodes' coordinates
    for x in next_word.nodes():
         next_word.nodes[x]['pos'] = positions[x]

    G = next_word
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        textposition = "top center",
        textfont_size = 10,
        mode = 'markers+text',
        #mode='markers',
        hoverinfo='text',
        hovertext = 'hovertext',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=False,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Word Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    node_hover = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(adjacencies[0])
        node_hover.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    node_trace.hovertext = node_hover

    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Mapping Each Word to Its Next Words',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

    py.plot(fig, filename='word_connections.html')
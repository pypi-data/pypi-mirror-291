import plotly.graph_objs as go
import networkx as nx


class GraphInteractive:
    def __init__(self, G):
        self.G = G

    def plot(self):
        pos = nx.random_layout(self.G)

        # edge
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line={'width': .5, 'color': '#010203'},
            hoverinfo='none',
            mode='lines'
        )
        for edge in self.G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        # node
        node_trace = go.Scatter(
            x=[],
            y=[],
            mode='markers',
            marker={
                'showscale': True,
                'colorscale': 'RdBu',
                'reversescale': False,
                'color': [],
                'size': 12,
                'colorbar': {
                    'thickness': 35,
                    'title': 'Node Connections',
                    'xanchor': 'left',
                    'titleside': 'right'
                },
                'line': {'width': 2}
            }
        )

        for node in self.G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])

        # add color to node points
        for node, adjacencies in enumerate(self.G.adjacency()):
            node_trace['marker']['color'] += tuple([len(adjacencies[1])])

        layout = go.Layout(
            title='Network Graph of Provider & Physician',
            titlefont={'size': 16},
            showlegend=False,
            margin={'b': 20, 'l': 5, 'r': 5, 't': 40},
            annotations=[{
                'showarrow': False,
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.005,
                'y': -0.002
            }],
            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False}
        )
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=layout
        )

        fig.show()

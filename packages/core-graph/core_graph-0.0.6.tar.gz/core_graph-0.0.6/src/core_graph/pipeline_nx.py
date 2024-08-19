import networkx as nx
import infomap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import polars as pl
from time import perf_counter


class GraphPipelineNX:
    def __init__(self, nx_graph=None):
        self.nx_graph = nx_graph

    def create_graph_from_similarity_matrix(self, similarity_matrix, threshold: float = 0.5):
        """
        Create network from similarity matrix
        cosine_similarity_matrix = np.array([
            [1.0, 0.8, 0.2],
            [0.8, 1.0, 0.5],
            [0.2, 0.5, 1.0]
        ])
        """
        self.g = nx.Graph()
        num_nodes = similarity_matrix.shape[0]

        # Add nodes
        for i in range(num_nodes):
            self.g.add_node(i)

        # Add edges based on the similarity threshold
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if similarity_matrix[i, j] >= threshold:
                    self.g.add_edge(i, j, weight=similarity_matrix[i, j])

        return self.nx_graph

    def find_communities(self):
        """
        Partition network with the Infomap algorithm.
        Annotates nodes with 'community' id and return number of communities found.
        """
        im = infomap.Infomap(two_level=True, silent=True)
        im.add_networkx_graph(self.nx_graph)
        im.run()
        print(f"[NX Infomap] Found {im.num_top_modules} modules with codelength {im.codelength:.8f} bits")

        communities = {node: module for node, module in im.modules}
        nx.set_node_attributes(self.nx_graph, communities, 'community')

        return self.nx_graph

    def centrality(self, prime_key: str = 'node_id', graph_mode: str = None, only_degree: bool = False):
        """
        graph_mode: None | directed
        """
        def _create_dataframe(dict_graph, prime_key: str = 'node_id', function: str = 'degree'):
            return pl.DataFrame({
                f'{prime_key}': list(dict_graph.keys()),
                f'{function}': list(dict_graph.values())
            })

        # list algorithm
        nodes_info_dict = {
            'eigenvector_centrality': nx.eigenvector_centrality_numpy,
            'betweenness_centrality': nx.betweenness_centrality,
            'closeness_centrality': nx.closeness_centrality,
            'katz_centrality': nx.katz_centrality_numpy,
        }
        if graph_mode == 'directed':
            nodes_info_dict.update({'pagerank': nx.pagerank})

        # algorithm
        dict_ = dict(nx.degree(self.nx_graph))
        nodes_info = _create_dataframe(dict_graph=dict_, prime_key=prime_key, function='degree')
        if only_degree:
            return nodes_info
        else:
            for i, f in nodes_info_dict.items():
                start = perf_counter()
                dict_ = dict(f(self.nx_graph))
                print(f'[Centrality] {i}: {perf_counter() - start:,.2f}s')
                tmp = _create_dataframe(dict_graph=dict_, prime_key=prime_key, function=i)
                nodes_info = nodes_info.join(tmp, on=prime_key, how='left')
            return nodes_info


class GraphPlotNX:
    def __init__(self, g, community: str = None):
        self.g = g
        self.community = community

    def _create_community_on_graph(self):
        communities = [v for k, v in nx.get_node_attributes(self.g, self.community).items()]
        numCommunities = max(communities) + 1

        # color map from http://colorbrewer2.org/
        cmapLight = colors.ListedColormap(
            ['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#cab2d6'],
            'indexed',
            numCommunities
        )
        cmapDark = colors.ListedColormap(
            ['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a'],
            'indexed',
            numCommunities
        )
        return communities, cmapLight, cmapDark

    def draw_network(self, fig_size: tuple = (10, 6), node_size: int = 20):
        """
        -- sample --
        pos = {
            2383884: array([-0.16682509,  0.01932504]),
            2433037: array([-0.03267272, -0.03621675])
        }
        nx.get_node_attributes(g, 'community') = {
            2383884: 281,
            2433037: 1174,
        }
        """
        # position map
        pos = nx.spectral_layout(self.g)

        # init config
        config = {
            'G': self.g,
            'pos': pos,
            'node_size': node_size
        }

        # community ids
        communities, cmapLight, cmapDark = None, None, None
        if self.community:
            communities, cmapLight, cmapDark = self._create_community_on_graph()
            config.update({
                'node_color': communities,
                'cmap': cmapLight
            })

        # draw
        fig, ax = plt.subplots(figsize=fig_size)
        nx.draw_networkx_edges(self.g, pos, ax=ax)
        nodeCollection = nx.draw_networkx_nodes(**config)

        if self.community:
            darkColors = [cmapDark(v) for v in communities]
            nodeCollection.set_edgecolor(darkColors)

import networkx as nx
import igraph as ig
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
from pathlib import Path
import polars as pl
from .func import time_decorator


class GraphPipelineIG:
    def __init__(self, ig_graph=None):
        self.ig_graph = ig_graph
        
    def create_network_from_dataframe(self, df, source: str, target: str, edge_attr: list, verbose: bool = True):
        """Create network from dataframe"""
        self.G = nx.from_pandas_edgelist(
            df,
            source,
            target,
            edge_attr
        )
        self.ig_graph = ig.Graph.from_networkx(self.G)
        if verbose:
            print(self.ig_graph.summary())
        return self.ig_graph

    def benchmark_find_communities(self):
        @time_decorator
        def find_communities_benchmark(function, graph, name):
            # run
            communities = function()
            lst = ['_community_fastgreedy', '_community_walktrap']
            if name in lst:
                communities = communities.as_clustering()
            modularity = graph.modularity(communities)
            stats = {
                'name': name,
                'modularity': modularity,
                'num_communities': len(communities),
            }
            return communities, stats

        lst = [
            self.ig_graph.community_infomap,
            self.ig_graph.community_fastgreedy,
            self.ig_graph.community_leading_eigenvector,
            self.ig_graph.community_label_propagation,
            self.ig_graph.community_multilevel,
            self.ig_graph.community_spinglass,
            self.ig_graph.community_walktrap,
        ]
        results = []
        for f in lst:
            name = f.__name__
            communities, stats = find_communities_benchmark(f, self.ig_graph, name)
            results.append(stats)
        return pl.DataFrame(results)


def geometric_median(points):
    """Compute the geometric median of a set of points."""
    def objective(point):
        return np.sum(np.linalg.norm(points - point, axis=1))

    initial_guess = np.median(points, axis=0)
    result = minimize(objective, initial_guess, method='BFGS')
    return result.x


def convex_hull_centroid(points):
    """Compute the centroid of the convex hull of a set of points."""
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    return np.mean(hull_points, axis=0)


class GraphPlotIG:
    def __init__(
            self,
            ig_graph,
            file_name: str = None,
            fig_size: tuple = (6, 4),
            save_path: Path = None
    ):
        self.ig_graph = ig_graph
        # config
        self.file_name = file_name
        self.fig_size = fig_size
        self.save_path = save_path

    def plot(self, visual_style: dict = None, large_graph: bool = False):
        # init
        init_visual_style = {'layout': 'kk'}
        if large_graph:
            init_visual_style = {
                'layout': self.ig_graph.layout_fruchterman_reingold(niter=1000, start_temp=10),
                'vertex_size': 3,  # Smaller nodes
                'edge_width': 0.1,  # Thinner edges
                'vertex_label': None
            }
        if visual_style:
            init_visual_style.update(visual_style)
        # plot
        fig, ax = plt.subplots(figsize=self.fig_size)
        ig.plot(self.ig_graph, target=ax, **init_visual_style)
        fig.tight_layout()
        return fig, ax

    def plot_cmap(
            self,
            node_values: list,
            visual_style: dict = None,
            cmap_label: str = '',
            colormap: str = 'viridis',
            add_color_bar: bool = False,
    ):
        cmap = mpl.colormaps[colormap]
        norm = Normalize(vmin=min(node_values), vmax=max(node_values))
        colors = [cmap(norm(degree)) for degree in node_values]

        if not visual_style:
            visual_style = {
                'vertex_color': colors,
                'vertex_size': 20,
                'edge_width': 0.5,
                'vertex_label': None
            }
        fig, ax = self.plot(visual_style)

        # add colorbar
        if add_color_bar:
            sm = ScalarMappable(cmap=cmap, norm=norm)
            cbar = plt.colorbar(sm, ax=ax)
            cbar.set_label(cmap_label)

    def plot_community(
            self,
            communities,
            mode: str = 'geo',
            add_label: bool = True,
            add_legend: bool = False,
    ):
        """
        mode: 'geo' | 'hull
        """
        # fig
        fig, ax = plt.subplots(figsize=self.fig_size)
        num_communities = len(communities)
        palette = ig.RainbowPalette(n=num_communities)
        # plot
        ig.plot(
            communities,
            target=ax,
            mark_groups=True,
            palette=palette,
            vertex_size=15,
            edge_width=0.5,
        )
        # layout
        layout = self.ig_graph.layout_fruchterman_reingold(
            niter=1000,
            start_temp=10,
        )
        layout_array = np.array(layout.coords)
        # draw
        if add_label:
            for i, community in enumerate(communities):
                community_layout = layout_array[community]
                # calculate label positions
                values = geometric_median(community_layout)
                match mode:
                    case 'hull':
                        values = convex_hull_centroid(community_layout)

                # add labels for the community
                ax.text(
                    values[0],
                    values[1],
                    f"C{i + 1}",
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7),
                    ha='center',
                    va='center',
                    fontweight='bold'
                )
        # add legend
        if add_legend:
            legend_handles = []
            for i in range(len(communities)):
                handle = ax.scatter(
                    [], [],
                    s=100,
                    facecolor=palette.get(i),
                    edgecolor="k",
                    label=i,
                )
                legend_handles.append(handle)

            ax.legend(
                handles=legend_handles,
                title='Community:',
                bbox_to_anchor=(0, 1.0),
                bbox_transform=ax.transAxes,
            )

        if self.save_path:
            fig.savefig(self.save_path)

    @staticmethod
    def plot_betweenness_cmap(g, vertex_betweenness, edge_betweenness, ax, cax1, cax2):
        """
        Plot vertex/edge betweenness, with colorbars

        Args:
            g: the graph to plot.
            ax: the Axes for the graph
            cax1: the Axes for the vertex betweenness colorbar
            cax2: the Axes for the edge betweenness colorbar
        """

        # Rescale betweenness to be between 0.0 and 1.0
        scaled_vertex_betweenness = ig.rescale(vertex_betweenness, clamp=True)
        scaled_edge_betweenness = ig.rescale(edge_betweenness, clamp=True)
        print(f"vertices: {min(vertex_betweenness)} - {max(vertex_betweenness)}")
        print(f"edges: {min(edge_betweenness)} - {max(edge_betweenness)}")

        # Define mappings betweenness -> color
        cmap1 = LinearSegmentedColormap.from_list("vertex_cmap", ["pink", "indigo"])
        cmap2 = LinearSegmentedColormap.from_list("edge_cmap", ["lightblue", "midnightblue"])

        # Plot graph
        g.vs["color"] = [cmap1(betweenness) for betweenness in scaled_vertex_betweenness]
        g.vs["size"] = ig.rescale(vertex_betweenness, (10, 50))
        g.es["color"] = [cmap2(betweenness) for betweenness in scaled_edge_betweenness]
        g.es["width"] = ig.rescale(edge_betweenness, (0.5, 1.0))
        ig.plot(
            g,
            target=ax,
            layout="fruchterman_reingold",
            vertex_frame_width=0.2,
        )

        # Color bars
        norm1 = ScalarMappable(norm=Normalize(0, max(vertex_betweenness)), cmap=cmap1)
        norm2 = ScalarMappable(norm=Normalize(0, max(edge_betweenness)), cmap=cmap2)
        plt.colorbar(norm1, cax=cax1, orientation="horizontal", label='Vertex Betweenness')
        plt.colorbar(norm2, cax=cax2, orientation="horizontal", label='Edge Betweenness')


# g = ig.Graph.Famous("Zachary")
# plot = GraphPlot(g)
# degrees = g.degree()
# GraphPlot(g, fig_size=(6, 4)).plot_cmap(degrees)

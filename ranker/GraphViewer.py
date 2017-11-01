import matplotlib.pyplot as plt
import networkx as nx


class GraphViewer(object):
    graph = "graphData.txt"
    number_of_nodes = 640

    def make_graph(self):
        G = nx.DiGraph()
        G.add_nodes_from(range(0, self.number_of_nodes))
        with open(self.graph, "r") as f:
            for line in f:
                n1, n2 = line.split(",")
                n1 = int(n1)
                n2 = int(n2)
                G.add_edge(n1, n2)
        return G

    def view_graph(self, node_list=[], ranks=None):
        graph = self.make_graph()
        node_list = list(set(node_list + range(0, 30)))
        sub_graph = graph.subgraph(node_list)
        if ranks is None:
            ranks = dict(sub_graph.in_degree())
        else:
            ranks = {k: v for k, v in enumerate(ranks)}
        nx.draw(sub_graph, nodelist=ranks.keys(), node_size=[v*50 for v in
                                                             ranks.values()])
        nx.draw(sub_graph, nx.spring_layout(sub_graph, k=10))
        plt.show()


if __name__ == "__main__":
    GraphViewer().view_graph()
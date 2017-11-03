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

    def view_graph(self, node_list=[], ranks=None, mult_factor=500, concat=100):
        graph = self.make_graph()
        val_map = {}
        for node in node_list:
            val_map[node] = 0.25
        node_list = list(set(node_list + range(0, 30)))
        sub_graph = graph.subgraph(node_list)
        values = [val_map.get(node, 1.0) for node in
                  sub_graph.nodes()]
        if ranks is None:
            ranks = dict(sub_graph.in_degree())
        else:
            temp_ranks = {k: v for k, v in enumerate(ranks)}
            ranks = dict(sub_graph.in_degree())
            for node in ranks.keys():
                ranks[node] = temp_ranks[node]
        nx.draw(sub_graph, nodelist=ranks.keys(),
                node_size=[v*mult_factor+concat for v in
                           ranks.values()],
                cmap=plt.get_cmap("jet"), node_color=values, alpha=0.5,
                pos=nx.spring_layout(sub_graph, k=10))
        if concat == 100:
            nx.draw_networkx_labels(sub_graph, labels=ranks, font_size=10,
                                    font_weight="bold", font_color="black",
                                    alpha=0.9,
                                    pos=nx.spring_layout(sub_graph, k=10))
        plt.show()
        plt.axis('off')


if __name__ == "__main__":
    pass
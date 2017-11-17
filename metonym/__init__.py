import math
import networkx as nx

MAX_LENGTH = 100


class WordNetGraph(object):
    def __init__(self, graph_file):
        self.graph = nx.read_adjlist(graph_file)

        # The name of the graph's "root" node, in reference to the taxonomy induced
        # by the hypernymy relation.
        self.root_name = 'entity.n.01'

        # The taxonomy depth is the maximum distance from the synset root (entity.n.01) to
        # any other synset that can be reached via any edges.
        lengths = list(nx.shortest_path_length(self.graph, self.root_name).values())
        self.taxonomy_depth = max(lengths)

    def shortest_path_distance(self, synset1, synset2):
        try:
            path = nx.shortest_path(self.graph, synset1.name(), synset2.name())
            #print(path)
            return len(path)
        except nx.NetworkXNoPath:
            return None

    def lch_similarity(self, synset1, synset2):
        distance = self.shortest_path_distance(synset1, synset2)
        if distance is None:
            distance = self.taxonomy_depth

        # Simulate the Leacock-Chodorow similarity measure by factoring in the depth of the taxonomy.
        return -math.log2(distance / (2 * self.taxonomy_depth))

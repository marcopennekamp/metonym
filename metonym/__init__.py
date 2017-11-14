import math
import networkx as nx

MAX_LENGTH = 100


class WordNetGraph(object):
    def __init__(self, graph_file):
        self.graph = nx.read_adjlist(graph_file)

        # The name of the graph's "root" node, in reference to the taxonomy induced
        # by the hypernymy relation.
        self.root_name = 'entity.n.01'

    def shortest_path_distance(self, synset1, synset2):
        try:
            path = nx.shortest_path(self.graph, synset1.name(), synset2.name())
            #print(path)
            return len(path)
        except nx.NetworkXNoPath:
            return None

    def path_similarity(self, synset1, synset2):
        distance = self.shortest_path_distance(synset1, synset2)
        if distance is None:
            distance = MAX_LENGTH

        # Simulate the Leacock-Chodorow similarity measure by taking the shortest path to
        # the entity.n.01 synset as the maximum depth of the taxonomy.
        # FIXME: The depth changes based on the current synsets, which isn't very good for a stable distance measure.
        def depth(synset):
            return nx.shortest_path_length(self.graph, synset.name(), self.root_name)
        taxonomy_depth = max([depth(synset1), depth(synset2)])
        return -math.log2(distance / (2 * taxonomy_depth))

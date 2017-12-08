from nltk.corpus import wordnet as wn
import math
import networkx as nx

MAX_LENGTH = 100
SYNSET_LEMMA_SEPARATOR = '//'


class Node:
    def __init__(self, synset, lemma):
        self.synset = synset
        self.lemma = lemma

    def key(self):
        return f'{self.synset.name()}{SYNSET_LEMMA_SEPARATOR}{self.lemma.name()}'

    @staticmethod
    def from_key(key):
        parts = key.split(SYNSET_LEMMA_SEPARATOR)
        synset = wn.synset(parts[0])
        return Node.from_synset_and_lemma_name(synset, parts[1])

    @staticmethod
    def from_synset_and_lemma_name(synset, lemma_name):
        lemmas = [lemma for lemma in synset.lemmas() if lemma.name() == lemma_name]
        assert len(lemmas) == 1, "There must be exactly one lemma with the correct name."
        return Node(synset, lemmas[0])


class WordNetGraph(object):
    def __init__(self, graph_file):
        self.graph = nx.read_gml(graph_file)

        # The name of the graph's "root" node, in reference to the taxonomy induced
        # by the hypernymy relation.
        self.root_name = f'entity.n.01{SYNSET_LEMMA_SEPARATOR}entity'

        # The taxonomy depth is the maximum distance from the synset root (entity.n.01) to
        # any other synset that can be reached via any edges.
        lengths = list(nx.shortest_path_length(self.graph, self.root_name, weight='weight').values())
        self.taxonomy_depth = max(lengths)

    def shortest_path(self, node1, node2):
        try:
            return nx.shortest_path(self.graph, node1.key(), node2.key(), weight='weight')
        except nx.NetworkXNoPath:
            return None

    def shortest_path_distance(self, node1, node2):
        try:
            return nx.shortest_path_length(self.graph, node1.key(), node2.key(), weight='weight')
        except nx.NetworkXNoPath:
            return None

    def lch_similarity(self, node1, node2):
        distance = self.shortest_path_distance(node1, node2)
        if distance is None:
            distance = self.taxonomy_depth

        # Simulate the Leacock-Chodorow similarity measure by factoring in the depth of the taxonomy.
        # We add 1 to the distance, because the distance of the same synsets is 0 and log(0) is not defined.
        return -math.log2((distance + 1) / (2 * self.taxonomy_depth))

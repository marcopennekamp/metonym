from nltk.corpus import wordnet as wn
from metonym import WordNetGraph
from argparse import ArgumentParser


def main(graph_file, word1, word2):
    graph = WordNetGraph(graph_file)
    synset1 = wn.synsets(word1)
    synset2 = wn.synsets(word2)
    print("\n===The meaning of each word sense===")
    for syn in synset1 + synset2:
        print("%s\t%s\t%s" % (syn.name, ":", syn.definition))
    print("\n===Comparing synset of one term with the synset of another===")
    for syn1 in synset1:
        for syn2 in synset2:
            print("%s\t%s\t%s" % (syn1.name, syn2.name, graph.path_similarity(syn1, syn2)))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", help="File where the wordnet graph is stored")
    parser.add_argument("word1", help="First word for comparing word sense")
    parser.add_argument("word2", help="Second word for comparing word sense")
    args = parser.parse_args()
    if args.word1 and args.word2 and args.file:
        main(args.file, args.word1, args.word2)

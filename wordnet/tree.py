from wordnet.utils import *
from stats.metrics import get_similarities


OBJECT = 'corgi.n.01'


class WordTree(object):
    def __init__(self, synset):
        if type(synset) == list:
            self.value = synset[0]
            self.children = synset[1:]
        else:
            self.value = synset
            self.children = synset.hyponyms()

    @property
    def child_nodes(self):
        return [WordTree(a) for a in self.children]

    @property
    def get_value(self):
        return self.value


def build_tree(root):
    object = wn.synset(root)
    word_tree = WordTree(object)

    objects = list(i for i in node_recurse_generator(word_tree))

    return objects


def main():
    OBJECT = input("What object? ")
    tree = build_tree(f"{OBJECT}.n.01")

    root = wn.synset('corgi.n.01')

    scores = {node.name().split('.')[0]: root.wup_similarity(node) for node in tree}

    for k in scores.keys():
        print(k, scores[k])

    return scores




if __name__ == "__main__":
    main()

import numpy as np

from nltk.corpus import wordnet as wn
from itertools import islice


def get_hyponyms(synset):
    hypo = lambda s: s.hyponyms()
    hyponyms = list(synset.closure(hypo))

    return hyponyms

def get_hypernyms(synset):
    hyper = lambda s: s.hypernyms()
    hypernyms = list(synset.closure(hyper))

    return hypernyms


# TODO (@messiest) generate the WordNet tree

def main(n=1):
    object = wn.synsets('corgi').pop()
    synsets = list(wn.all_synsets('n'))
    np.random.shuffle(synsets)
    synsets_ = (i for i in synsets)
    i = 1
    for s in synsets_:
        if object in get_hyponyms(s):
            print(f"Hyponyms: {s}")
        if object in get_hypernyms(s):
            print(f"Hypernyms: {s}")
        i += 1


if __name__ == "__main__":
    main(500)

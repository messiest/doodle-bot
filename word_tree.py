from nltk.corpus import wordnet as wn


OBJECT = 'vertebrate.n.01'


class WordTree(object):
    def __init__(self, synset):
        if type(synset) == list:
            self.value = synset[0]
            self.children = synset[1:]
        else:
            self.value = synset
            self.children = synset.hyponyms()

    @property
    def child_elements(self):
        return [WordTree(a) for a in self.children]

    @property
    def get_value(self):
        return self.value


def node_recurse_generator(node):
    yield node.value
    for n in node.child_elements:
        yield from node_recurse_generator(n)


def clean(synset_name):
    name = synset_name.split('.')[0]
    name = name.replace('_', ' ')

    return name


def main(root=OBJECT):
    object = wn.synset(root)
    word_tree = WordTree(object)

    objects = list(clean(i.name()) for i in node_recurse_generator(word_tree))

    for i in objects:
        print(i)

    return objects


if __name__ == "__main__":
    x = main()

    print(x)

from nltk.corpus import wordnet as wn


def node_recurse_generator(node):
    yield node.value
    for n in node.child_nodes:
        yield from node_recurse_generator(n)


def clean(synset_name):
    name = synset_name.split('.')[0]
    name = name.replace('_', ' ')

    return name



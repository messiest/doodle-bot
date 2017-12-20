import numpy as np
from nltk.corpus import wordnet as wn

from s3.bucket import S3Bucket


BUCKET = 'doodle-bot'


def get_name(synset):
    name = synset.name.split('.')[0]

    return name


def total_objects(bucket, n):
    total = len(bucket.objects)

    return total


def total_categories(bucket):
    keys = bucket.get_keys()
    f = lambda key: key.split('/')[1]  # get the sub directory name

    unique_keys = list({f(key) for key in keys})

    print(unique_keys)

    return unique_keys


def get_objects(bucket, n):  # TODO (@messiest) get objects from sampler object
    syns = [wn.synset(f"{i.key.split('/')[1]}") for i in bucket.objects if i.key.split('/')[1] != '']
    syns = np.random.choice(syns, n)

    return syns


def get_similarities(objects, root=wn.synset('corgi.n.01')):

    total_similarities = {obj: root.wup_similarity(obj) for obj in set(objects)}

    return total_similarities


def main():
    base_line = wn.synset('dog.n.01')

    s3 = S3Bucket(BUCKET)
    # objects = get_objects(s3, 10000)
    #
    # similarities = get_similarities(objects, root=base_line)

    x = total_categories(s3)

    return x


if __name__ == "__main__":
    x = main()

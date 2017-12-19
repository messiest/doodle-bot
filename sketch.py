import numpy as np

from s3.bucket import S3Bucket
from nltk.corpus import wordnet as wn


BUCKET = 'doodle-bot'


def get_objects(n):
    global s3
    syns = [wn.synset(f"{i.key.split('/')[1]}.n.01") for i in s3.objects if i.key.split('/')[1] != '']
    syns = np.random.choice(syns, n)

    return syns


if __name__ == "__main__":
    base_line = wn.synset('corgi.n.01')
    s3 = S3Bucket(BUCKET)
    objects = get_objects(100)

    total_similarities = [base_line.wup_similarity(obj) for obj in set(objects)]

    print(np.mean(total_similarities))

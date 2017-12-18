import os
import string
import numpy as np
from imagenet_downloads.image_downloads import get_image_urls
from get_images import get_images
from nltk.corpus import wordnet as wn
from s3.bucket import S3Bucket


"""
This file constructs the classifier model.
"""

BUCKET = 'doodle-bot'


class ImageSampler:

    def __init__(self, object, bucket=None):
        self.name = object
        print(f"Base object is: {self.name}")
        if bucket: self.source = S3Bucket(bucket)

        self.base = wn.synsets(self.name).pop()

    def check_path(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def sample_synsets(self, n=10, root=None):
        sample = []

        if root:

            synsets =
        else:
            synsets = list(wn.all_synsets('n'))
        while len(sample) < n:
            s = np.random.choice(synsets, 1)[0]
            if s.name() != self.name and s not in sample:
                sample.append(s)

        return sample

    def get_object_tree(self, synset):

        hypo = lambda s: s.hyponyms()
        hyper = lambda s: s.hypernyms()

        hyponyms = list(synset.closure(hypo))
        hypernyms = list(synset.closure(hyper))

        print(f"{hyponyms}, {hypernyms}")

def main():
    print("In main()...")
    sampler = ImageSampler('corgi', bucket=BUCKET)
    sample = sampler.sample_synsets(10)

    for s in sample:
        sampler.get_object_tree(s)
        name = s.name().split('.')[0]
        name_ = name.replace('_', ' ')

        print(f"Name: {name}, {name_}")


if __name__ == "__main__":
    main()

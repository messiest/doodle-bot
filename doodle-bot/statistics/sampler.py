"""
Various sampler utilities
"""
import os
import numpy as np
import imagenet.downloads as img
from nltk.corpus import wordnet as wn
from s3.bucket import S3Bucket
from wordnet.tree import build_tree


BUCKET = 'doodle-bot'


class ImageSampler:

    def __init__(self, object, bucket=None):
        self.name = object
        print(f"Base object is: {self.name}")
        if bucket: self.source = S3Bucket(bucket)

        self.base = wn.synsets(self.name).pop()

        self.key_store = None

        self.pos_images = {}
        self.neg_images = {}

    def check_path(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def get_image_categories(self, root_class, support_class=None, n=100):
        """
        Get images that aren't in the base class, but isolated by the support class.
        """
        sample = build_tree(root_class)
        if support_class:
            print(f"Removing base class for support: {support_class}")
            support = build_tree(support_class)
            sample = [i for i in sample if i not in support]
        sample = list(set(np.random.choice(sample, n)))

        return sample

    def gather_images(self, n=1000, base=True):
        sample = self.get_image_categories('vertebrate.n.01', 'dog.n.01', n)
        existing_images = self.source.get_keys()
        for s in sample:
            if base:
                s = self.name
            for key, url, tag in img.get_images(s):
                if key not in existing_images:
                    self.source.download_image(key, url, tag)
                else:
                    print("File already exists.")

    def pull_down_images(self, n=1000):
        """

        :param n:
        :type n:
        :return:
        :rtype:
        """
        def read_key(key):
            split = key.split('/')
            return split

        objects = self.source.get_keys()  # TODO(@messiest) this needs to be changed to return a sample
        print(f"{len(objects)} Objects")

        np.random.shuffle(objects)

        self.key_store = {}  #

        for o in objects:
            _, obj, file = read_key(o)
            if obj == self.name:
                if obj not in self.pos_images.keys():
                    self.pos_images[obj] = []
                self.pos_images[obj].append(file)
            else:
                if obj not in self.neg_images.keys():
                    self.neg_images[obj] = []
                self.neg_images[obj].append(file)

        return self.pos_images, self.neg_images


def main():
    print("Running sampler.main()...")
    sampler = ImageSampler('corgi', bucket=BUCKET)

    l = build_tree('dog.n.01')

    print(l)

    # sampler.gather_images(base=True)
    # sampler.gather_images(base=False)

    pos, neg = sampler.pull_down_images()
    print(pos)

    keys = sampler.key_store
    for k in keys.keys():
        print(f"Key: {k}, Files: {len(keys[k])}")




if __name__ == "__main__":
    main()

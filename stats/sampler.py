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
        def read_key(key):
            split = key.split('/')
            return split

        objects = self.source.get_keys()
        print(f"{len(objects)} Objects")
        self.key_store = {}

        for o in objects:
            loc, obj, file = read_key(o)
            if obj not in self.key_store.keys():
                self.key_store[obj] = []
            self.key_store[obj].append(file)

        class_1 = []  # TODO(@messiest) convert these to dictionaries
        class_0 = []

        for j in self.key_store.keys():
            if j == self.name:
                for m in self.key_store[j]:
                    if len(class_1) == n:
                        break
                    class_1.append(m)
            else:
                for m in self.key_store[j]:
                    if len(class_0) == n:
                        break
                    class_0.append(m)

        return class_1, class_0


def main():
    print("Running sampler.main()...")
    sampler = ImageSampler('corgi', bucket=BUCKET)

    l = build_tree('physical_object.n.01')

    print(l)

    # sampler.gather_images(base=True)
    # sampler.gather_images(base=False)

    sampler.pull_down_images()
    keys = sampler.key_store
    for k in keys.keys():
        print(f"Key: {k}, Files: {len(keys[k])}")




if __name__ == "__main__":
    main()

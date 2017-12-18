import os
import string
import numpy as np
import imagenet_downloads.image_downloads as img
from get_images import get_images
from nltk.corpus import wordnet as wn
from s3.bucket import S3Bucket
from word_tree.word_tree import build_tree



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

    def get_image_categories(self, support_class, root_class, n=10):
        """
        Get images that aren't in the base class, but isolated by the support class.

        """
        support = build_tree(support_class)
        root = build_tree(root_class)

        not_positive = [i for i in root if i not in support]
        positive = list(set(np.random.choice(support, n)))

        not_positive = list(set(np.random.choice(not_positive, n)))

        return positive, not_positive

    def fetch_images(self, base=True):

        _, sample = self.get_image_categories('dog.n.01', 'vertebrate.n.01', 100)

        existing_images = self.source.get_keys()

        for s in sample:
            if base:
                s = self.name
            for key, url, tag in img.get_images(s, num_images=None):
                if key not in existing_images:
                    self.source.download_image(key, url, tag)
                else:
                    print("File already exists.")



def main():
    print("In main()...")
    sampler = ImageSampler('corgi', bucket=BUCKET)
    sampler.fetch_images(base=False)



if __name__ == "__main__":
    main()

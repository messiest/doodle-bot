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


class ImageClassifier:

    def __init__(self, object, bucket=None):
        self.name = object
        if bucket: self.source = S3Bucket(bucket)

    def check_path(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def sample_synsets(self, n=10):
        sample = []
        synsets = list(wn.all_synsets('n'))
        while len(sample) < n:
            s = np.random.choice(synsets, 1)[0]
            if s.name() != self.name and s not in sample:
                sample.append(s)

        return sample

    def sample_from_bucket(self, n=10, is_object=False):
        print(f"Getting {is_object} images...")
        self.sample = []
        while len(self.sample) < n:
            image_file = self.source.sample(n).pop()  # return single object from list
            file_split = image_file.split('/')

            if is_object:
                if file_split[1] == self.name:
                    self.sample.append(image_file)

            else:
                if file_split[1] != self.name:
                    self.sample.append(image_file)

        return self.sample

    def get_data(self, true_class=True):
        sample = self.sample_from_bucket(100, is_object=true_class)
        for s in sample:
            path = s.split('/')
            file = path.pop(-1)
            path = '/'.join(path) + "/"
            self.check_path(path)
            if true_class:
                file_path = f"{path}/{file}"
            else:
                file_path = f"{path}/{file}"

            if not os.path.exists(file_path):
                self.source.download_file(s, file_path)

    def download_images_to_bucket(self, object, n=10):
        """
        save image file to bucket from url

        :param bucket:
        :type bucket:
        :param object:
        :type object:
        :return:
        :rtype:
        """
        bucket = self.source
        existing_images = bucket.keys
        urls = get_image_urls(object)

        image_urls = []

        for i, url in enumerate(urls):
            for j in string.whitespace:
                url = url.replace(j, '')  # drop whitespace characters

            if url:
                split_url = url.split('/')
                key = f"images/{object}/{split_url[-1]}"  # construct key

                _, extension = os.path.splitext(key)  # get file extension

                if key not in existing_images and extension == ".jpg":  # skip existing images and non-jpg images
                    print(f"{i+1}: {key}")
                    bucket.download_image(key, url)
                    image_urls.append(url)
                else:
                    print(f"{i+1}: {key} already exists.")

            if i == n:
                break

        return image_urls


def main():
    model = ImageClassifier('corgi', bucket=BUCKET)

    sample = model.sample_synsets(10)

    print("HERE " * 25)

    for s in sample:
        name = s.name().split('.')[0]
        name_ = name.replace(' ', '_')

        print("Name: ", name)

        for image in model.download_images_to_bucket(name_):
            print("Image: ", image)
            file = image.split('/')[-1]
            key = f"images/{name}/{file}"

            print(f"Key: {key}, File: {file}")

            model.source.download_file(key, image)


if __name__ == "__main__":
    main()

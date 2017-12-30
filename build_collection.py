import os
import sys
import string
import numpy as np
from imagenet.downloads import get_image_urls
from nltk.corpus import wordnet as wn
from s3.bucket import S3Bucket


"""
This file constructs the classifier model.
"""

IMG_DIR = 'images'
BUCKET = 'cifar-extended'
CIFAR10 = ['airplane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']  # automobile changed to car


class ImageClassifier:

    def __init__(self, bucket=None):
        if bucket: self.source = S3Bucket(bucket)

    def check_path(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def sample_synsets(self, n=10):  # TODO (@messiest) adjust to sample from a single synset
        sample = []
        synsets = list(wn.all_synsets('n'))
        while len(sample) < n:
            s = np.random.choice(synsets, 1)[0]

        return sample

    def sample_from_bucket(self, n=10, is_object=False):
        print(f"Sampling {n} images from bucket...")
        self.sample = []
        while len(self.sample) < n:
            image_file = self.source.sample(n).pop()  # return single object from list
            file_split = image_file.split('/')

            self.sample.append(image_file)

        return self.sample

    def get_data(self, n=100):
        sample = self.sample_from_bucket(n)
        for s in sample:
            path = s.split('/')
            file = path.pop(-1)
            path = '/'.join(path) + "/"

            if path.split('/')[1] not in CIFAR10:
                print("ERROR PATH: ", path)
                continue

            self.check_path(path)

            file_path = f"{path}/{file}"

            if not os.path.exists(file_path):
                self.source.download_file(s, file_path)

    def download_images_to_bucket(self, object, n=1000):
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
        np.random.shuffle(urls)  # randomize order

        image_urls = []

        for i, url in enumerate(urls):
            for j in string.whitespace:
                url = url.replace(j, '')  # drop whitespace characters

            if url:
                split_url = url.split('/')
                key = f"{IMG_DIR}/{object}/{split_url[-1]}"  # construct key

                _, extension = os.path.splitext(key)  # get file extension

                if key not in existing_images and extension == ".jpg":  # skip existing images and non-jpg images
                    print(f"{i+1}: {key}")
                    bucket.download_image(key, url, object)
                    image_urls.append(url)

                if extension != ".jpg":
                    print("incorrect file type: ", extension)
                    continue

                if key in existing_images:
                    print(f"{key} already exists.")
                    continue

                else:
                    print("Unknown error.")
                    continue

            if i == n:
                break

        return image_urls


def get_image_files():
    files = {obj: os.listdir(f'{IMG_DIR}/{obj}/') for obj in os.listdir(f'{IMG_DIR}/') if obj[-4:] == '.jpg'}

    return files


def main(n=10000, new_images=True):
    model = ImageClassifier(bucket=BUCKET)

    pattern = ".n.01"
    sample_space = [wn.synset(i+pattern) for i in CIFAR10]

    if new_images:
        for s in sample_space:
            name = s.name().split('.')[0]
            name_ = name.replace(' ', '_')

            print("Name: ", name)

            downloads = model.download_images_to_bucket(name_, n=10)

            for image in downloads:
                print("Image: ", image)
                file = image.split('/')[-1]
                key = f"images/{name}/{file}"

                print(f"Key: {key}, File: {file}")

                model.source.download_file(key, image)

    # print(model.sample_from_bucket(10))

    model.get_data(n=n)

    print("DONE")
    return



if __name__ == "__main__":
    print("Build extended CIFAR10 image collection...")
    try:
        main(int(sys.argv[1]))
    except IndexError:
        main(n=100)

    files = get_image_files()
    for label in files.keys():
        print(label, len(files[label]))

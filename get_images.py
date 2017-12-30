import os
import string
import numpy as np
from nltk.corpus import wordnet
from s3.bucket import S3Bucket
from imagenet.downloads import get_image_urls


"""

"""

BUCKET = 'cifar-extended'
CIFAR10 = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


def get_images(bucket, object, n=1000):
    """
    save image file to bucket from url

    :param bucket:
    :type bucket:
    :param object:
    :type object:
    :return:
    :rtype:
    """
    bucket = S3Bucket(bucket)
    existing_images = bucket.keys
    urls = get_image_urls(object)
    print(len(urls))
    urls = [url for url in urls if url[-4:]]  # only .jpg images
    print(len(urls))
    quit()
    np.random.shuffle(urls)

    print(f"Object: {object}")

    for i, url in enumerate(urls):
        for j in string.whitespace:
            url = url.replace(j, '')  # drop whitespace characters
        if url:
            split_url = url.split('/')
            key = f"images/{object}/{split_url[-1]}"  # construct key

            _, extension = os.path.splitext(key)  # get file extension

            print("EXTENSION ", extension)

            if key not in existing_images and extension == ".jpg":  # skip existing images and non-jpg images
                print(f"{key}")
                bucket.download_image(key, url, tag=object)
            else:
                print(f"{key} already exists.")

        if i == n:
            break


if __name__ == "__main__":
    # BUCKET = input("Input S3 Bucket Name: ")
    # OBJECT = input("\tObject: ")
    for obj in CIFAR10:
        print("OBJECT: ", obj)
        get_images(BUCKET, obj, 10)

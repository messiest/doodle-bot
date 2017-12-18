import os
import string
from nltk.corpus import wordnet
from s3.bucket import S3Bucket
from imagenet_downloads.image_downloads import get_image_urls


"""

"""

BUCKET = 'doodle-bot'
OBJECT = 'corgi'


def get_images(bucket, object):
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

    for url in urls:
        for i in string.whitespace:
            url = url.replace(i, '')  # drop whitespace characters
        if url:
            split_url = url.split('/')
            key = f"images/{object}/{split_url[-1]}"  # construct key

            _, extension = os.path.splitext(key)  # get file extension

            if key not in existing_images and extension == ".jpg":  # skip existing images and non-jpg images
                print(f"{key}")
                bucket.download_image(key, url)
            else:
                print(f"{key} already exists.")


if __name__ == "__main__":
    BUCKET = input("Input S3 Bucket Name: ")
    OBJECT = input("\tObject: ")
    get_images(BUCKET, OBJECT)

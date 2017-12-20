import numpy as np
import boto3
import botocore
import requests


class S3Bucket:
    """
    wrapper for connecting to an s3 bucket instance
    """
    def __init__(self, name, printer=False):
        self.name = name
        self.printer = printer
        self.bucket = self.connect()
        self.objects = self.get_objects()
        self.keys = self.get_keys()

    def connect(self):
        """
        connect to s3 instance
        """
        print("Connecting to: <{}>...".format(self.name))
        s3 = boto3.resource('s3')
        _bucket = s3.Bucket(self.name)
        exists = True
        try:
            s3.meta.client.head_bucket(Bucket=self.name)
        except botocore.exceptions.ClientError as error:
            error_code = int(error.response['Error']['Code'])
            if error_code == 404:  # bucket does not exist.
                print("{} - Bucket does not exist.".format(error_code))
                exists = False

        if self.printer:
            print("bucket <{}> exists? {}".format(self.name, exists))

        return _bucket

    def get_objects(self):
        """
        get list of objects in s3 bucket

        :return: a list of s3 objects in the bucket
        :rtype: list
        """
        print(f"Getting objects in <{self.name}>...")
        self.objects = [object for object in self.bucket.objects.all()]

        return self.objects

    def get_keys(self):
        """
        get list of file names in s3 bucket

        :return: self.keys
        :rtype: list
        """
        print(f"Getting keys in <{self.name}>...")
        self.keys = [obj.key for obj in self.objects if obj.key[-1] != '/']

        return self.keys

    def sample(self, n):
        """
        return random sample of n objects from s3 bucket
        
        :param n: number of items
        :type n: int
        :return: sample
        :rtype: list
        """
        # print("Generating sample from object...")
        try:
            sample = list(np.random.choice(self.keys, n))

        except ValueError:
            sample = []

        return sample

    def download_image(self, key, url, tag):
        """
        download an image to an s3 bucket

        :param key: key for the image
        :type key: str
        :param url: url for the image
        :type url: str
        :return: True/False for if the download succeeded
        :rtype: bool
        """

        try:
            print("\tdownloading from url: ", url)
            image = requests.get(url, stream=True, timeout=3)  # stream image from url
            self.bucket.put_object(Key=key, Body=image.raw.read(), Tagging=f"object={tag}")  # upload to s3

            return True

        except:
            print("image did not save")
            return False

    def download_file(self, key, file_name):
        """
        download file image

        :param key:
        :type key:
        :param file_name:
        :type file_name:
        :return:
        :rtype:
        """
        print(f"   downloading from bucket: {key}")
        try:
            with open(file_name, 'wb') as data:
                self.bucket.download_fileobj(key, data)
        except FileNotFoundError:
            pass


def main():
    bucket = S3Bucket('doodle-bot')
    filenames = bucket.keys
    print(len(filenames))


if __name__ == "__main__":
    main()

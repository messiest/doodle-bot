import os
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


def main():
    model = ImageClassifier('corgi', bucket=BUCKET)
    model.get_data()
    model.get_data(true_class=False)




if __name__ == "__main__":
    main()
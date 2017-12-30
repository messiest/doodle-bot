import os

from s3.bucket import S3Bucket


IMG_DIR = 'images'
BUCKET = 'cifar-extended'
CIFAR10 = ['airplane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']  # automobile changed to car


def check_path(path):
    _dir = os.path.dirname(path)
    if not os.path.exists(_dir):
        os.makedirs(_dir)


def download_images(bucket, n=100):
    sample = bucket.sample(n)

    for s in sample:
        path = s.split('/')
        file = path.pop(-1)
        path = '/'.join(path) + "/"

        if path.split('/')[1] not in CIFAR10:
            print("ERROR PATH: ", path)
            continue

        check_path(path)
        file_path = f"{path}/{file}"

        if not os.path.exists(file_path):
            bucket.download_file(s, file_path)


def build_data(keys):
    data_dict = {}
    for k in keys:
        path = k.split('/')
        label = path[1]
        if label not in data_dict.keys():
            data_dict[label] = []
        data_dict[label].append(k)

    return data_dict


def main():
    bucket = S3Bucket(BUCKET)
    download_images(bucket, 5000)


if __name__ == "__main__":
    main()

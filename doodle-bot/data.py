import os
import sys
import numpy as np


# sys.path.append('../')
DATA_DIR = 'images/'


def get_image_data():
    data_dict = {}
    labels = os.listdir(DATA_DIR)
    for label in labels:
        path_ = f"{DATA_DIR}{label}/"
        if label not in data_dict.keys():
            data_dict[label] = [path_ + img for img in os.listdir(path_)]  # dictionary of lists for data return

    return data_dict


def get_image_files(n=None):
    files = []
    data_dict = get_image_data()

    for obj in data_dict.keys():
        for file in data_dict[obj]:
            files.append(file)

    np.random.shuffle(files)

    if n:
        return files[:n]

    else:
        return files


if __name__ == "__main__":
    data = get_image_files()
    print(data)

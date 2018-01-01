import numpy as np

from data import get_image_data

pass

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


def main(n=100):
    image_files = get_image_files()

    return image_files


if __name__ == "__main__":
    print(main())

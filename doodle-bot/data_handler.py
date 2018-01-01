import os
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt


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


def get_label_tuples(files):
    """
    get named tuples of (tag, image)

    """
    tagged = []
    for img in files:
        tag = img.split('/')[1]
        tagged.append((tag, img))

    return tagged


def build_trainer(files, resize=False, size=[256, 256]):
    filename_queue = tf.train.string_input_producer(files, shuffle=False)  # queue for the file names

    file_reader = tf.WholeFileReader()  # file reader object for image files
    key, value = file_reader.read(filename_queue)  # read the files

    # TODO(@messiest) understand difference b/w decode_jpeg and decode_image
    img = tf.image.decode_jpeg(value, channels=3, try_recover_truncated=True,
                               acceptable_fraction=0.05)  # decode image file
    img = tf.image.convert_image_dtype(img, tf.float32)  # cast to tf.float32

    if resize:
        img = tf.image.resize_images(img, size)  # resize the image

    return img


def run_session(image_files, previews=None):
    n = len(image_files)

    trainer = build_trainer(image_files, resize=True, size=[64, 64])

    with tf.Session() as sess:
        coord = tf.train.Coordinator()  # instantiate the training coordinator
        threads = tf.train.start_queue_runners(coord=coord)  # populate the filename queue

        #         y = tf.placeholder(np.object)

        for i, (tag, file) in enumerate(get_label_tuples(image_files)):  # iterate over files

            try:
                image = sess.run(trainer)

                yield image

            except:
                print("deleting ", file)
                os.remove(file)  # delete files with loading errors
                continue

            if previews and i % n // previews == 0:  # display every every n/10th image
                print("\nFile: ", file)
                print("Tag: ", tag)
                print("Dimensions: ", image.shape)  # output image array shape
                plt.imshow(image)  # display image
                plt.axis('off')  # don't display the axes
                plt.show()  # display each image

        coord.request_stop()
        coord.join(threads)


def main():
    data = get_image_files(10)
    print(data)
    for i in run_session(data, 1):
        print(i, "###" * 40)


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import numpy as np
import os
import cv2
import nltk


IMG_PATH = "images/"


def get_image_urls(search_item):
    """
    return image urls from https://www.image-net.org

    :param search_item: WNID to search for
    :type search_item: str
    """

    print(f"Getting {search_item} image urls...")
    url = "http://www.image-net.org/search?q={}".format(search_item)                    # search image by wnid
    html = requests.get(url)                                                            # url connect
    soup = BeautifulSoup(html.text, 'lxml')                                             # create soup object
    tags = []
    for search in soup.findAll(name='table', attrs={'class', 'search_result'}):         # find table
        for a in search.findAll(name='a'):                                              # find href tag
            try:                                                                        # prevent breaking
                tags.append(a['href'].split('?')[1])                                    # href w/ wnid link
                break                                                                   # only get first wnid
            except IndexError:
                pass

    image_urls = []

    print("TAGS: ", tags)

    for tag in tags:
        # print(f"tag: {tag}")
        url = "http://www.image-net.org/api/text/imagenet.synset.geturls?{}".format(tag)  # image net search id
        try:
            html = requests.get(url)                                                      # html for search
            urls = (image_url for image_url in html.text.split('\r\n'))
            for img_url in urls:
                image_urls.append(img_url)
        except:
            pass

    return image_urls


def url_to_image(url):
    """
    download image from url

    :param url: image url
    :type url: str
    :return: image
    :rtype: OpenCV image
    """
    # while True:  # why?
    try:
        resp = requests.get(url, timeout=3, stream=True)                             # break in case of a load error
        image = np.asarray(bytearray(resp.raw.read()), dtype="uint8")                # convert to numpy array
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)                                # read the color image
        return image                                                                 # return the image
    except requests.exceptions.ReadTimeout:
        return "ERROR"                                                               # error return


def download_images_to_bucket(search, num_images=None):
    """
    search for images on ImageNet, write images to s3

    :param search: term to search ImageNet for
    :type search: str
    :param num_images: total number of images to download
    :type num_images: int
    """
    if isinstance(search, nltk.corpus.reader.wordnet.Synset):
        search = search.name().split('.')[0].replace('_', ' ')                           # get object name from synset

    print("\nSearching for {} images...".format(search))
    search_url = search.replace(' ', '+').replace(',', '%2C').replace("'", "%27")        # formatted for search url
    search = search.replace(', ', '-').replace(' ', '_').replace("'", "")                # formatted for file system

    image_urls = [url for url in get_image_urls(search_url)]                             # get list of image urls
    total_urls = len(image_urls)
    print("  {} image urls found".format(total_urls))

    for i, url in enumerate(image_urls):                         # start with last used url
        if i == num_images:
            break
        file = url.split('/')[-1]                                # image file name
        if file.split('.')[-1] != "jpg":           # skip non jpg
            continue
        print(f" {i+1}/{total_urls} - {file}")
        key = "images/{}/{}".format(search, file)  # path for image file

        yield key, url, search

        # bucket.download_image(key, url, search)


def image_search(search_terms, images=1000):
    """
    perform image search for provided list of WNIDs

    :param search_terms: search terms
    :type search_terms: list
    :param images: number of images to download
    :type images: int
    """
    for search in search_terms:                                                         # iterate over searches
        if search not in os.listdir("images/") or len(os.listdir("images/")) < images:  # ignore populated categories
            # get_images(search, num_images=images)                                       # get the images
            pass


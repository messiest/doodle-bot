import sampler as S
import imagenet_downloads.image_downloads as img

sampler = S.ImageSampler('corgi')

_, sample = sampler.get_image_categories('dog.n.01', 'vertebrate.n.01', 100)

for i in sample:
    print(i)

    for a, b, c in img.get_images(i, num_images=5):
        print(a, b, c)


    quit()

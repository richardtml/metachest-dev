""" resize.py """

from os import makedirs
from os.path import isdir, join, isfile
from pprint import pprint

import pandas as pd
# import skimage as ski
from dask import delayed, compute
from PIL import Image
from skimage.transform import resize
from tqdm.dask import TqdmCallback

from common import read_toml


def verify_image(src):
    if not isfile(src):
        return src


def center_crop(image):
    w, h = image.size
    if w != h:
        if w < h:
            offset = (h - w) // 2
            image = image.crop((0, offset+w, w, offset))
        else:
            offset = (w - h) // 2
            image = image.crop((offset, h, offset+h, 0))
    return image


def resize_image(src, dst, size):
    image = ski.io.imread(src)
    image = center_crop(image)
    image = resize()


# def center_crop(image):
#     h, w = image.shape
#     if h != w:
#         if h < w:
#             offset = (w - h) // 2
#             image = image[:, offset:h+offset]
#         else:
#             offset = (h - w) // 2
#             image = image[offset:w+offset, :]
#     return image


# def resize_image(src, dst, size):
#     image = ski.io.imread(src)
#     image = center_crop(image)
#     image = resize()



def resize_dataset(size=384):

    config = read_toml('config.toml')
    images_dir = join(config['metachest'], f'images-{size}')
    if isdir(images_dir):
        print(f'Images dir already exists: {images_dir}')
        return

    # makedirs(images_dir)
    dst_dir = {}
    for ds in {'chex', 'mimic', 'nih', 'padchest'}:
        dst_dir[ds] = join(images_dir, ds)
        # makedirs(dst_dir[ds])

    src_dir = {
        'chex': join(config['chex'], 'CheXpert-v1.0'),
        'mimic': join(config['mimic'], 'images'),
        'nih': join(config['nih'], 'images'),
        'padchest': join(config['padchest'], 'images')
    }

    src_fmt = {
        'chex': 'jpg',
        'mimic': 'jpg',
        'nih': 'png',
        'padchest': 'png'
    }

    df = pd.read_csv('metachest.csv')
    df = df[:100]

    src_paths, dst_paths = [], []
    for row in df.itertuples():
        src_path = join(src_dir[row.dataset], f'{row.name}.{src_fmt[row.dataset]}')
        dst_path = join(dst_dir[row.dataset], f'{row.name}.jpg')
        src_paths.append(src_path)
        dst_paths.append(dst_path)

    print('Verifying all images are available:')
    delayeds = []
    for src_path in src_paths:
        delayeds.append(delayed(verify_image)(src_path))
    with TqdmCallback():
        results = compute(delayeds)[0]
    results = [r for r in results if r]
    if results:
        print('Verify the datasets, the following images were not found:')
        pprint(results)
        return

    print('Resizing images:')
    delayeds = []
    for src_path, dst_path in zip(src_paths, dst_paths):
        delayeds.append(delayed(resize_image)(src_path, dst_path, size))
    with TqdmCallback():
        results = compute(delayeds)


def main():
    resize_dataset()

if __name__ == '__main__':
    main()

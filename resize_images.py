""" resize.py """

from os import makedirs
from os.path import isdir, isfile, dirname, join
from pprint import pprint

import pandas as pd
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
            # left, upper, right, lower
            image = image.crop((0, offset, w, offset+w))
        else:
            offset = (w - h) // 2
            # left, upper, right, lower
            image = image.crop((offset, 0, offset+h, h))
    return image


def crop_resize_image(src, dst, size):
    try:
        image = Image.open(src)
        image = image.convert('L')
        image = center_crop(image)
        image = image.resize((size, size), Image.LANCZOS)
        makedirs(dirname(dst), exist_ok=True)
        image.save(dst)
    except BaseException as be:
        print(be)
        return src


def resize_dataset(size=384):

    config = read_toml('config.toml')
    images_dir = join(config['metachest_dir'], f'images-{size}')
    if isdir(images_dir):
        print(f'Images dir already exists: {images_dir}')
        return

    makedirs(images_dir)
    dst_dir = {}
    for ds in {'chestxray14', 'chexpert', 'mimic', 'padchest'}:
        dst_dir[ds] = join(images_dir, ds)
        makedirs(dst_dir[ds])

    src_dir = {
        'chestxray14': join(config['chestxray14_dir'], 'images'),
        'chexpert': join(config['chexpert_dir'], 'CheXpert-v1.0'),
        'mimic': join(config['mimic_dir'], 'images'),
        'padchest': join(config['padchest_dir'], 'images')
    }

    src_fmt = {
        'chestxray14': 'png',
        'chexpert': 'jpg',
        'mimic': 'jpg',
        'padchest': 'png'
    }

    df = pd.read_csv('metachest.csv')
    # df = df.sample(10000)

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
        delayeds.append(delayed(crop_resize_image)(src_path, dst_path, size))
    with TqdmCallback():
        results = compute(delayeds)[0]
    results = [r for r in results if r]
    if results:
        print('There were errors processing the following images:')
        pprint(results)
        return


def main():
    resize_dataset()

if __name__ == '__main__':
    main()

""" resize.py """

from os import makedirs
from os.path import isfile, dirname, join
from pprint import pprint

import numpy as np
import pandas as pd
from dask import delayed, compute
from PIL import Image
from tqdm.dask import TqdmCallback

from common import read_toml


def verify_image(src):
    if not isfile(src):
        return src


def convert(image):
    if image.mode == 'I;16':
        array = np.uint8(np.array(image) / 256)
        return Image.fromarray(array)
    else:
        return image.convert('L')


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
        image = convert(image)
        image = center_crop(image)
        image = image.resize((size, size), Image.LANCZOS)
        makedirs(dirname(dst), exist_ok=True)
        image.save(dst)
    except BaseException as be:
        print(be)
        return src


def resize_dataset(size=384):

    print(f'Resizing dataset images to {size}')

    config = read_toml('config.toml')
    images_dir = join(config['metachest_dir'], f'images-{size}')

    makedirs(images_dir, exist_ok=True)
    dst_dir = {}
    for ds in {'chestxray14', 'chexpert', 'mimic', 'padchest'}:
        dst_dir[ds] = join(images_dir, ds)
        makedirs(dst_dir[ds], exist_ok=True)

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


    df = pd.read_csv(join(config['metachest_dir'], 'metachest.csv'))
    nf_df = pd.read_csv(join(config['metachest_dir'], 'metachest_nf.csv'))
    df = pd.concat([
        df[['dataset', 'name']],
        nf_df[['dataset', 'name']]
    ])
    # df = df.sample(1000)

    src_paths, dst_paths = [], []
    for row in df.itertuples():
        src_path = join(src_dir[row.dataset], f'{row.name}.{src_fmt[row.dataset]}')
        dst_path = join(dst_dir[row.dataset], f'{row.name}.jpg')
        if not isfile(dst_path):
            src_paths.append(src_path)
            dst_paths.append(dst_path)

    print('  Verifying images availability:')
    delayeds = []
    for src_path in src_paths:
        delayeds.append(delayed(verify_image)(src_path))
    with TqdmCallback():
        results = compute(delayeds)[0]
    results = [r for r in results if r]
    if results:
        print('  Verify the datasets, the following images were not found:')
        pprint(results)
        return

    print('  Resizing images:')
    delayeds = []
    for src_path, dst_path in zip(src_paths, dst_paths):
        delayeds.append(delayed(crop_resize_image)(src_path, dst_path, size))
    with TqdmCallback():
        results = compute(delayeds)[0]
    results = [r for r in results if r]
    if results:
        print('  There were errors processing the following images:')
        pprint(results)
        return


if __name__ == '__main__':
    import fire
    fire.Fire(resize_dataset)

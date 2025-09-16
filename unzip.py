
import zipfile

from tqdm.auto import tqdm

def unzip(src, dst):
    with zipfile.ZipFile(src, 'r') as zip_ref:
        for file in tqdm(iterable=zip_ref.namelist(), total=len(zip_ref.namelist())):
            zip_ref.extract(member=file, path=dst)

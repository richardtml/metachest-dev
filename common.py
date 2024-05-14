
import tomllib
import tomli_w


MIN_AGE, MAX_AGE = 10, 80
AGE_INTERVAL = (MIN_AGE, MAX_AGE)

CHEX_PATHOLOGIES = [
    'atelectasis',
    'cardiomegaly',
    'consolidation',
    'edema',
    'effusion',
    'lung_opacity',
    'pneumonia',
    'pneumothorax',
]

MIMIC_PATHOLOGIES = [
    'atelectasis',
    'cardiomegaly',
    'consolidation',
    'edema',
    'effusion',
    'lung_opacity',
    'pneumonia',
    'pneumothorax',
]

CHESTXRAY14_PATHOLOGIES = [
    'atelectasis',
    'cardiomegaly',
    'consolidation',
    'edema',
    'effusion',
    'emphysema',
    'fibrosis',
    'hernia',
    'infiltration',
    'mass',
    'nodule',
    'pleural_thickening',
    'pneumonia',
    'pneumothorax',
]

PADCHEST_PATHOLOGIES = [
    'atelectasis',
    'cardiomegaly',
    'consolidation',
    'edema',
    'effusion',
    'emphysema',
    'fibrosis',
    'hernia',
    'infiltration',
    'mass',
    'nodule',
    'pleural_thickening',
    'pneumonia',
    'pneumothorax',
]


MTRN = [
    'effusion',
    'lung_opacity',
    'atelectasis',
    'infiltration',
    'nodule',
    'mass',
    'pleural_thickening'
]

MVAL = [
    'emphysema',
    'fibrosis',
    'hernia'
]

MTST = [
    'cardiomegaly',
    'edema',
    'pneumothorax',
    'consolidation',
    'pneumonia'
]

MCLASSES = {'mtrn': MTRN, 'mval': MVAL, 'mtst': MTST}


def filter_msets(df, filter_df, mclasses):
    mset_exclude = {
        'mtrn': mclasses['mval'] + mclasses['mtst'],
        'mval': mclasses['mtst'],
        'mtst': mclasses['mval'],
    }
    for mset, classes in mset_exclude.items():
        exclude = df[classes].any(axis=1)
        filter_df.loc[exclude, mset] = 0
    return filter_df


def read_toml(path):
    with open(path, 'rb') as f:
        return tomllib.load(f)


def save_toml(path, data):
    with open(path, mode='wb') as f:
        tomli_w.dump(data, f)

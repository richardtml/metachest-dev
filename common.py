
import tomllib


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


def read_toml(path):
    with open(path, 'rb') as f:
        return tomllib.load(f)

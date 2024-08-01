import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import pandas as pd
import seaborn as sns
import tomllib

from matplotlib.ticker import EngFormatter


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


ALIASES = {
    'dataset': 'Dataset',

    'chestxray14': 'ChestX-ray14',
    'chexpert': 'CheXpert',
    'metachest': 'MetaChest',
    'mimic': 'MIMIC',
    'padchest': 'PadChest',

    'mtrn': 'Meta-Train',
    'mval': 'Meta-Validation',
    'mtst': 'Meta-Test',

    'atelectasis': 'Atelectasis',
    'cardiomegaly': 'Cardiomegaly',
    'consolidation': 'Consolidation',
    'edema': 'Edema',
    'effusion': 'Effusion',
    'emphysema': 'Emphysema',
    'fibrosis': 'Fibrosis',
    'hernia': 'Hernia',
    'infiltration': 'Infiltration',
    'lung_opacity': 'Lung opacity',
    'mass': 'Mass',
    'nodule': 'Nodule',
    'pleural_thickening': 'Pleural thickening',
    'pneumonia': 'Pneumonia',
    'pneumothorax': 'Pneumothorax',

    'age': 'Age',
    'sex': 'Sex',
    'view': 'View',

    'total': 'Total',
}


# def filter_msets(df, filter_df, mclasses):
#     mset_exclude = {
#         'mtrn': mclasses['mval'] + mclasses['mtst'],
#         'mval': mclasses['mtst'],
#         'mtst': mclasses['mval'],
#     }
#     for mset, classes in mset_exclude.items():
#         exclude = df[classes].any(axis=1)
#         filter_df.loc[exclude, mset] = 0
#     return filter_df


def filter_mset(mset, mclasses, df, n_metadata_cols=5):
    mval_mtst_examples = df[mclasses['mval'] + mclasses['mtst']].any(axis=1)
    if mset == 'mtrn':
        # keep examples with only mtrn classes
        mtrn_only_examples = ~mval_mtst_examples
        df = df[mtrn_only_examples]
        classes = mclasses['mtrn']
    else:
        # discarding examples with only mtrn classes
        df = df[mval_mtst_examples]
        # keep examples with mtrn+mset clases
        mtrn_mset_classes = mclasses['mtrn'] + mclasses[mset]
        mtrn_mset_examples = df[mtrn_mset_classes].any(axis=1)
        df = df[mtrn_mset_examples]
        classes = mtrn_mset_classes
    cols = list(df.columns[:n_metadata_cols]) + classes
    df = df[cols]
    return df


def plot_coocc(dataset, mset, df):
    df = df.fillna(0).astype(int, copy=True)
    df_mat = df.to_numpy()
    coocc_mat = df_mat.T.dot(df_mat)

    paths = [ALIASES[p] for p in df.columns]
    coocc = pd.DataFrame(coocc_mat, index=paths, columns=paths)
    mask = np.triu(coocc+1, k=1)

    fig, ax = plt.subplots(figsize=(10, 5))
    trans_offset = mtransforms.offset_copy(ax.transData, fig=fig, x=0.18)

    sns.heatmap(
        coocc,
        linewidth=1,
        cmap='RdPu',
        annot=True,
        annot_kws={"fontsize": 'x-small', 'ha': 'right',
                   'transform': trans_offset},
        fmt='g',
        cbar_kws={'label': 'Number of images with both pathologies',
                  'format': EngFormatter()},
        mask=mask,
        ax=ax
    )

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=30, horizontalalignment='right')
    ax.figure.axes[-1].tick_params(labelsize='x-small')

    plt.title(f'Pathology co-ocurrence matrix of {dataset} in {ALIASES[mset]}')
    plt.tight_layout()



# def read_mclasses(path='mtl_classes.toml'):
#     mclasses = read_toml(path)
#     return {
#         'mtrn': mclasses['mtrn'],
#         'mval': mclasses['mval'],
#         'mtst': mclasses['mtst']
#     }


def read_toml(path):
    with open(path, 'rb') as f:
        return tomllib.load(f)



# def save_toml(path, data):
#     with open(path, mode='wb') as f:
#         tomli_w.dump(data, f)

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import pandas as pd
import seaborn as sns
import tomllib

from matplotlib.ticker import EngFormatter
from matplotlib_venn import venn3


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


def _filter_mset(mset, mclasses, df, n_metadata_cols=5):
    """ Filter df for the given mset:

        | mset | definition     |
        |------|----------------|
        | mtrn | (mval ∪ mtst)' |
        | mval | mval ∩ mtst'   |
        | mtst | mval' ∩ mtst   |

        See mtl_complete.ipynb
    """
    mtrn_classes = mclasses['mtrn']
    mval_classes = mclasses['mval']
    mtst_classes = mclasses['mtst']
    mval_mask = df[mval_classes].any(axis=1)
    mtst_mask = df[mtst_classes].any(axis=1)

    if mset == 'mtrn':
        # (mval ∪ mtst)'
        mset_mask = ~(mval_mask | mtst_mask)
        mset_classes = mtrn_classes
    elif mset == 'mval':
        # mval ∩ mtst'
        mset_mask = mval_mask & ~mtst_mask
        mset_classes = mtrn_classes + mval_classes
    else:
        # mval' ∩ mtst
        mset_mask = ~mval_mask & mtst_mask
        mset_classes = mtrn_classes + mtst_classes

    df = df[mset_mask].copy()
    cols = list(df.columns[:n_metadata_cols]) + mset_classes
    df = df[cols]
    return df


def plot_venn(mset):
    """ Venn diagram representation of _filter_mset()."""

    plt.figure(figsize=(2, 2))
    diagram = venn3((1, 1, 1, 1, 1, 1, 1),
                    set_labels=('mval\nclasses',
                                'mtst\nclasses',
                                'mtrn\nclasses'))
    for sid in ("100", "010", "110", "001", "101", "011", "111"):
        diagram.get_label_by_id(sid).set_text('')
        diagram.get_patch_by_id(sid).set_color('white')

    if mset == 'mtrn':
        color = '#1f77b4'
        diagram.get_patch_by_id('001').set_color(color)
    elif mset == 'mval':
        color = '#9467bd'
        diagram.get_patch_by_id('100').set_color(color)
        diagram.get_patch_by_id('101').set_color(color)
    else:
        color = '#e377c2'
        diagram.get_patch_by_id('010').set_color(color)
        diagram.get_patch_by_id('011').set_color(color)

    for sid in ("100", "010",  "001", "111"):
        diagram.get_patch_by_id(sid).set_edgecolor('black')

    for i in range(3):
        diagram.set_labels[i].set_fontsize('small')

    plt.title(f'{mset}\ndataset')
    plt.show()


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


def read_toml(path):
    with open(path, 'rb') as f:
        return tomllib.load(f)

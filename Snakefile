from os.path import join

from common import read_toml


config = read_toml('config.toml')
metachest_dir = config['metachest_dir']
mtl_dir = join(metachest_dir, 'mtl')
run_nb = "jupyter nbconvert --execute --to notebook --inplace"


def flatten(list_of_lists):
    return [item for row in list_of_lists for item in row]


mtl_complete_files = [
    join(mtl_dir, 'complete.csv'),
    join(mtl_dir, 'complete.toml')
]
mtl_subpop_files = flatten([
    [
        join(mtl_dir, f'{subpop}.csv'),
        join(mtl_dir, f'{subpop}.toml')
    ]
    for subpop in ['age_center', 'age_tails',
                   'sex_female', 'sex_male',
                   'view_ap', 'view_pa']
])
mtl_subds_files = flatten([
    [
        join(mtl_dir, f'ds_{dataset}.csv'),
        join(mtl_dir, f'ds_{dataset}.toml')
    ]
    for dataset in ['chestxray14', 'chexpert', 'mimic', 'padchest']
])


rule all:
    input:
        mtl_complete_files + mtl_subpop_files + mtl_subds_files

rule mtl_subpop:
    input:
        join(metachest_dir, 'metachest.csv')
    output:
        mtl_subpop_files
    shell:
        f"{run_nb} notebooks/mtl_subpop.ipynb"

rule mtl_subds:
    input:
        join(metachest_dir, 'metachest.csv')
    output:
        mtl_subds_files
    shell:
        f"{run_nb} notebooks/mtl_subds.ipynb"

rule mtl_complete:
    input:
        join(metachest_dir, 'metachest.csv')
    output:
        mtl_complete_files
    shell:
        f"{run_nb} notebooks/mtl_complete.ipynb"

rule metachest:
    input:
        [
            join(metachest_dir, f'{dataset}.csv')
            for dataset in ['chestxray14', 'chexpert', 'mimic', 'padchest']
        ]
    output:
        join(metachest_dir, 'metachest.csv')
    shell:
        f"{run_nb} notebooks/metachest.ipynb"

rule chestxray14:
    input:
        config['chestxray14_dir']
    output:
        join(metachest_dir, 'chestxray14.csv')
    shell:
        f"{run_nb} notebooks/chestxray14.ipynb"

rule chexpert:
    input:
        config['chexpert_dir']
    output:
        join(metachest_dir, 'chexpert.csv')
    shell:
        f"{run_nb} notebooks/chexpert.ipynb"

rule mimic:
    input:
        config['mimic_dir']
    output:
        join(metachest_dir, 'mimic.csv')
    shell:
        f"{run_nb} notebooks/mimic.ipynb"

rule padchest:
    input:
        config['padchest_dir']
    output:
        join(metachest_dir, 'padchest.csv')
    shell:
        f"{run_nb} notebooks/padchest.ipynb"

rule images:
    input:
        [join(metachest_dir, f'images-{res}')
         for res in [224, 384, 512, 768, 1024]]

rule images_224:
    input:
        [config['chestxray14_dir'], config['chexpert_dir'],
         config['mimic_dir'], config['padchest_dir']]
    output:
        directory(join(metachest_dir, f'images-{224}'))
    shell:
        f"python resize_images.py {224}"

rule images_384:
    input:
        [config['chestxray14_dir'], config['chexpert_dir'],
         config['mimic_dir'], config['padchest_dir']]
    output:
        directory(join(metachest_dir, f'images-{384}'))
    shell:
        f"python resize_images.py {384}"

rule images_512:
    input:
        [config['chestxray14_dir'], config['chexpert_dir'],
         config['mimic_dir'], config['padchest_dir']]
    output:
        directory(join(metachest_dir, f'images-{512}'))
    shell:
        f"python resize_images.py {512}"

rule images_768:
    input:
        [config['chestxray14_dir'], config['chexpert_dir'],
         config['mimic_dir'], config['padchest_dir']]
    output:
        directory(join(metachest_dir, f'images-{768}'))
    shell:
        f"python resize_images.py {768}"

rule images_1024:
    input:
        [config['chestxray14_dir'], config['chexpert_dir'],
         config['mimic_dir'], config['padchest_dir']]
    output:
        directory(join(metachest_dir, f'images-{1024}'))
    shell:
        f"python resize_images.py {1024}"

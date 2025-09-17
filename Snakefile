from os.path import join

from common import read_toml


config = read_toml('config.toml')
metachest_dir = config['metachest_dir']
distro_dir = join(metachest_dir, 'distro')
run_nb = "jupyter nbconvert --execute --to notebook --inplace"


def flatten(list_of_lists):
    return [item for row in list_of_lists for item in row]

subpop_files = [
    join(distro_dir, f'{subpop}.csv')
    for subpop in [
        'age_decade2', 'age_decade3', 'age_decade4', 'age_decade5',
        'age_decade6', 'age_decade7', 'age_decade8',
        'sex_female', 'sex_male',
        'view_ap', 'view_pa'
    ]
]
subds_files = [
    join(distro_dir, f'ds_{dataset}.csv')
    for dataset in ['chestxray14', 'chexpert', 'mimic', 'padchest']
]


rule all:
    input:
        [join(metachest_dir, 'metachest.csv')] + subpop_files + subds_files

rule distro_subpop:
    input:
        join(metachest_dir, 'metachest.csv')
    output:
        subpop_files
    shell:
        f"{run_nb} notebooks/distro_subpop.ipynb"

rule distro_subds:
    input:
        join(metachest_dir, 'metachest.csv')
    output:
        subds_files
    shell:
        f"{run_nb} notebooks/distro_subds.ipynb"

rule distro_complete:
    input:
        join(metachest_dir, 'metachest.csv')
    shell:
        f"{run_nb} notebooks/distro_complete.ipynb"

rule metachest:
    input:
        [
            join(metachest_dir, f'{dataset}.csv')
            for dataset in ['chestxray14', 'chexpert', 'mimic', 'padchest']
        ]
    output:
        [
            join(metachest_dir, 'metachest.csv'),
            join(metachest_dir, 'metachest_nf.csv')
        ]
    shell:
        f"{run_nb} notebooks/metachest.ipynb"

rule chestxray14:
    input:
        config['chestxray14_dir']
    output:
        [
            join(metachest_dir, 'chestxray14.csv'),
            join(metachest_dir, 'chestxray14_nf.csv')
        ]
    shell:
        f"{run_nb} notebooks/chestxray14.ipynb"

rule chexpert:
    input:
        config['chexpert_dir']
    output:
        [
            join(metachest_dir, 'chexpert.csv'),
            join(metachest_dir, 'chexpert_nf.csv')
        ]
    shell:
        f"{run_nb} notebooks/chexpert.ipynb"

rule mimic:
    input:
        config['mimic_dir']
    output:
        [
            join(metachest_dir, 'mimic.csv'),
            join(metachest_dir, 'mimic_nf.csv')
        ]
    shell:
        f"{run_nb} notebooks/mimic.ipynb"

rule padchest:
    input:
        config['padchest_dir']
    output:
        [
            join(metachest_dir, 'padchest.csv'),
            join(metachest_dir, 'padchest_nf.csv')
        ]
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

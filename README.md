# MetaChest

MetaChest is publicly available dataset patology classification on chest radiographs generated from ChestX-ray14, CheXpert, MIMIC-CXR-JPG and PadChest datasets.

![Metachest distribution](metachest.jpg)

## Datasets Setup

1. Create separate directories to store the datasets:
    ```bash
    mkdir {chestxray14_dir}
    mkdir {chexpert_dir}
    mkdir {mimic_dir}
    mkdir {padchest_dir}
    mkdir {metachest_dir}
    ```
    Specify the directories in the `config.toml` file.

2. Download and extract the datasets following the instructions on their websites. The following files are needed.

    * [ChestX-ray14](https://nihcc.app.box.com/v/ChestXray-NIHCC/folder/36938765345). Download `Data_Entry_2017_v2020.csv` and `batch_download_zips.py`, then run:
        ```bash
        cd {chexpert_dir}
        python batch_download_zips.py
        ```
        Extract all `images_*.tar.gz` files.

    * [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/). Download the full dataset, we recommend using [`azcopy`](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10?tabs=dnf).
        ```bash
        azcopy cp {provided_url} {chexpert_dir} --recursive
        ```

    * [MIMIC](https://physionet.org/content/mimic-cxr-jpg/2.0.0/). Download the full dataset.

    * [PadChest](https://bimcv.cipf.es/bimcv-projects/padchest/). Download the full dataset, we recommend using [`rclone`](https://rclone.org/install/).
        ```bash
        rclone -vP copy {provided_url} {padchest_dir}
        ```

2. Create and activate the enviroment.
    ```bash
    conda env create -f env.yml
    conda activate metachest
    ```

3. Generate the final `metachest.csv` dataset file:
    ```bash
    snakemake -c1
    ```


## Resizing images

To resize images from all datasets:

    ```bash
    snakemake -R images -c1
    ```

The images will be stored on the `metachest_dir` directory.

# MetaChest

MetaChest is publicly available dataset of chest radiographs and patologies generated from ChestX-ray14, CheXpert, MIMIC-CXR-JPG and PadChest datasets.

![Metachest distribution](metachest.jpg)

## Datasets Setup

1. Create and activate the enviroment.
```bash
conda env create -f env.yml
conda activate metachest
```

2. Specify in the `config.toml` file a download directory for each one of the datasets, we recommend the use of one directory per dataset. Also create and specify a directory for MetaChest.

3. Download the datasets following the instructions in their correspoding websites.

    * [ChestX-ray14](https://nihcc.app.box.com/v/ChestXray-NIHCC/folder/36938765345).

    * [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/). The use of `azcopy` is recommended:
    ```bash
    azcopy cp {provided_url} {chexpert_dir} --recursive
    ```

    * [MIMIC](https://physionet.org/content/mimic-cxr-jpg/2.0.0/).

    * [PadChest](). The use of `rclone` is recommended:
    ```bash
    rclone -vP copy {provided_url} {padchest_dir}
    ```

4. Extract the datasets.

5. Run the following to generate the final `metachest.csv` dataset file:
```bash
bash generate_metachest.sh
```


## Resizing images

To resize images from all datasets to a new size (e.g. 384) run:

```bash
python resize_images.py 384
```

The images will be stored on the `metachest_dir` directory.

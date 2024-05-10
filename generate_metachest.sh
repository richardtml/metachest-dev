#!/bin/bash

datasets=('chestxray14' 'chexpert' 'mimic' 'padchest' 'metachest')

for dataset in "${datasets[@]}"; do
    echo "Generating ${dataset}.csv"
    jupyter nbconvert --execute --to notebook --inplace ${dataset}.ipynb
done

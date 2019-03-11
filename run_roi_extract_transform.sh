#! /bin/bash

#bash roi_mni_extract.sh
python roi_transforms_mni2t1.py
bash roi_merge_lr_vd.sh

#extras
python run_mvpa_1.sh
python run_mvpa_2.sh
python run_mvpa_3.sh

python run_mvpa_blk_1.sh
python run_mvpa_blk_2.sh
python run_mvpa_blk_3.sh

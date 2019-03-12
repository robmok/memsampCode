#! /bin/bash
# runs roi extract, transform and merging scripts

bash roi_mni_extract.sh
python roi_transforms_mni2t1.py
bash roi_merge_lr_vd.sh

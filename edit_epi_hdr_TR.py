#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 16:14:01 2019

@author: robert.mok
"""
import numpy as np
import os
import glob
import nibabel as nib
from nibabel.testing import data_path

bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
os.chdir(bidsDir)

subs = range(3,34) #33 subs - range doesn't include last number
for iSub in subs:
    subNum=f'{iSub:02d}'
    print('Running sub-%02d' % iSub)
    fnames    = os.path.join(bidsDir, "sub-" + subNum, 'func', "*." + 'nii')
    #fnames    = os.path.join(bidsDir, "sub-" + subNum, 'func', "*." + 'nii.gz')
    datafiles = glob.glob(fnames)
    
    for iFile in datafiles:
        n1_img = nib.load(iFile)
        n1_header = n1_img.header
        #print(n1_header)
        n1_header['pixdim'][4] = 2.8
        nib.save(n1_img, os.path.join(iFile))
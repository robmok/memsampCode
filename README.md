# Memsamp - Abstract Category Signal

Bash and Python code for: Mok & Love, 2021, Abstract Neural Representations of Category Membership beyond Information Coding Stimulus or Response. Journal of Cognitive Neuroscience. https://doi.org/10.1162/jocn_a_01651

## Software and packages

FSL version:
Python version:

Python packages:
- numpy
- pandas
- scipy
- scikit-learn
- nibabel
- nilearn
- pandas
- nipype (mainly for ANTS when transforming ROIs)
- subprocess (to call functions at the cmd line from python)

Other requirements:
- dcm2niix
- jq (to edit json files)

## Scripts

Scripts used prior to pre-processing:
- dcm2bids_RM.sh - tranform dicom to nii format in bids style
- deface_memsamp.sh - deface structure MRIs
- edit_epi_hdr_TR.py - edit TR in header file to 2.8s
- mk_event_files_bids.py - for bids, though possibly event files are unused
- mk_event_files_bids_after_ran_once.py - as above script creates timing files, here just loads them
- move-non-bids-compliant-files.sh - removed some files - I think mainly from when I tried some FSL-based preprocessing, which were not used
- organize_epi_task_loc.sh - rename epi task files to bids format
- roi_MD_extract.sh - extracting ROIs from the MD network (FSL)
- roi_merge_lr_vd.sh - merging some ROIs (FSL)
- roi_transforms_mni2t1.py - transform ROIs from mni to T1 space
- sed_jsons.sh - editing info in jsons

Scripts for pre-processing and main analysis
- behav_model.py - script with behavioural model to estimate subjective category bound for each participant
- fmriprep_RM.sh - preprocessing pipeline (fMRIPrep)
- memsamp_RM.py - functions for organising conditions, distance measures
- mvpa_memsamp.py - script to run mvpa for ROIs, MAIN analyses
- run_feat_main_T1space_trialwise.sh - 1st level glm, estimates of single trials, results input into decoding analyses (MAIN analyses)

Plot and inspect results
- behav_memsamp.py - script to load in behavioural data, model-fit category bounds and plot it (figure 3B)
- check_mvpa_roi_results.py - script for t-test and multiple comparison correction over ROIS (FDR)
- plot_roi_decoding.py - plot MVPA ROI results, MAIN analyses. (note to self: - plot_roi_memsamp.py is an old version of this)

Not in paper:
- mvpa_searchlight_memsamp.py - searchlight analyses
- randomise_searchlight.sh - script to randomise searchlight results 
- run_feat_group.sh - 1st level glm (univariate)
- run_feat_main_T1space.sh - 1st level glm, estimates of blocks
- sl_subtractSearchLights_subjCat.py - searchlight, subtract subjCat images from subjCatOrth (orthgonal category bound directions
- sl_transforms_t12mni.py - searchlight, transfer from t1 space to mni space

# fMRI data on openneuro.org

https://openneuro.org/datasets/ds004009

doi:10.18112/openneuro.ds004009.v1.0.0 

# Data on OSF

Behavioural data / model:
- modelsubjcatfinal.pkl - model fitted subjective category bounds for each participant
- sub-01_task-memsamp_run-01_events.tsv - example full events file with behavioural responses  (example for a subject 01 and run 01) - load these files in to plot behaviour and fit model
- subjCat.pkl - info with subject category bounds for each participant

fMRI data (MVPA, ROI-based results):



# General pipeline

- organise behavioural data, fit behavioural model to get individual participant subjective category bounds, plot (python)
- prepare fMRI data into BIDS format, adding info to json files (bash, python)
- run preprocessing with fMRIPrep
- prepare ROI masks for individual participants (python, FSL)
- run 1st level GLMs with FSL (FEAT)
- run decoding analyses (MVPA using SVMs) on ROIs (python, scikit-learn), and statistics



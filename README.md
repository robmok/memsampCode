# Memsamp - Abstract Category Signal

Bash and Python code for: Mok & Love, 2021, Abstract Neural Representations of Category Membership beyond Information Coding Stimulus or Response. Journal of Cognitive Neuroscience.

## Software and packages

Python version:
packages:

- numpy
- pandas
- scipy
- scikit-learn


## Scripts

Scripts used prior to pre-processing:
dcm2bids_RM.sh - tranform dicom to nii format in bids style
deface_memsamp.sh - deface structure MRIs
edit_epi_hdr_TR.py - edit TR in header file to 2.8s
mk_event_files_bids.py - for bids, though possibly event files are unused
mk_event_files_bids_after_ran_once.py - as above script creates timing files, here just loads them
move-non-bids-compliant-files.sh - removed some files - I think mainly from when I tried some FSL-based preprocessing, which were not used
organize_epi_task_loc.sh - rename epi task files to bids format
roi_MD_extract.sh - extracting ROIs from the MD network (FSL)
roi_merge_lr_vd.sh - merging some ROIs (FSL)
roi_transforms_mni2t1.py - transform ROIs from mni to T1 space
sed_jsons.sh - editing info in jsons

Scripts for pre-processing and main analysis
behav_model.py - script with behavioural model to estimate subjective category bound for each participant
fmriprep_RM.sh - preprocessing pipeline (fMRIPrep)
mvpa_memsamp.py - script to run mvpa for ROIs, MAIN analyses
run_feat_main_T1space_trialwise.sh - 1st level glm, estimates of single trials, results input into decoding analyses (MAIN analyses)

Plot and inspect results
behav_memsamp.py - script to load in behavioural data, model-fit category bounds and plot it (figure 3B)
check_mvpa_roi_results.py - script for t-test and multiple comparison correction over ROIS (FDR)
plot_roi_decoding.py - plot MVPA ROI results, MAIN analyses. (note to self: plot_roi_memsamp.py is an old version of this)

Not in paper:
mvpa_searchlight_memsamp.py - searchlight analyses
randomise_searchlight.sh - script to randomise searchlight results 
run_feat_group.sh - 1st level glm (univariate)
run_feat_main_T1space.sh - 1st level glm, estimates of blocks
sl_subtractSearchLights_subjCat.py - searchlight, subtract subjCat images from subjCatOrth (orthgonal category bound directions
sl_transforms_t12mni.py - searchlight, transfer from t1 space to mni space


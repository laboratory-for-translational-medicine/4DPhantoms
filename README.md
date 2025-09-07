This repository provides the source code for generating 4D image phantoms.
**The corresponding input data and synthesized datasets are available at the following link:**
[here](https://www.cs.torontomu.ca/~elodie.lugez/data/)

Please note that some folders are very large.

1. Datasets A and B:
   - Folder names: A_4D_CT, B_4D_MR
   - Contents:
       * Input image data
       * Synthesized 4D image phantoms
       * Corresponding 4D multi-organ segmentations
	   
2. Dataset C:
   - Folder name: C_4D_MR
   - Contents:
       * Input image data
       * Additional 3D images acquired with alternative imaging parameters
       * Synthesized 4D MR image phantoms
	   
3. Dataset C Ground Truth DVFs:
   - Folder name: C_DVFs_4D_MR
   - Contents: Ground truth displacement vector fields (DVFs) for dataset C
   - Notes: This is a very large dataset
   
4. Source 4D Lung Inputs:
   - Folder name: Source_4D_Lung
   - Contents:
       * Collated 4D lung images
       * Computed 4D DVFs
   - Notes: Original input images used to generate the phantom datasets


Instructions:
-------------
- It is recommended to run changeOrientation2LPS.py first if planning to extract 2D sagittal or coronal images.
- Use the main pipeline (main.py) along with utils_4d.py and config_4d.py to process the data and synthesize cine images.
- Ensure that all datasets (A_4D_CT, B_4D_MR, C_4D_MR, and Source_4D_Lung) are placed in the same folder as the code so that the paths are correctly recognized.


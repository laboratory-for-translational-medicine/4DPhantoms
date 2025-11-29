# main.py
"""
Main pipeline for DVF propagation and cine synthesis.
"""

import gc
from pathlib import Path
import time

import numpy as np
import SimpleITK as sitk

from config_4d import CT_BASE_PATH, A_4D_CT_CASES, B_4D_MR_CASES, C_4D_MR_CASES
from utils_4d import (
    get_anatomical_orientation,
    force_orthogonal,
    propagate_dvf,
    get_trace_direction,
    assign_magnitude_to_dvfs,
    interpolate_dvfs_directional,
    moving_average_dvfs,
    load_and_prepare_img_seg,
    extract_slices,
    synthesize_cine,
    create_output_dirs
)

APPLICATION = 'C_4D_MR'  # Options: 'A_4D_CT', 'B_4D_MR', 'C_4D_MR'
extract_sagittal_coronal = True #True if user wants to extract sagittal and coronal images, False otherwise

def process_case(case_id: int):
    print("Processing case", case_id)
    """
    Process a single case: load images, propagate DVFs, and synthesize cine.
    """
    # Setup paths
    img_dir = Path(__file__).resolve().parent / APPLICATION / f"Data{case_id}"
    trace_file = img_dir / f"OriginalTrace{case_id}.csv"

    # Configuration from external module
    cfg = cases.get(case_id)
    if cfg is None:
        raise ValueError(f"No configuration for case {case_id}")

    ct_path = CT_BASE_PATH / cfg["subdir"] / cfg["file"]
    image_ct = sitk.ReadImage(str(ct_path))
    if image_ct.GetPixelID() > 8:
        image_ct = sitk.Cast(image_ct, sitk.sitkFloat32)

    # Load and prepare MR and segmentation images
    image, segmentation = load_and_prepare_img_seg(img_dir, image_ct, APPLICATION)

    # Load and propagate DVFs
    global time_propagate_dvfs
    start_time = time.time()
    dvfs, dvfs_ct = load_and_propagate_dvfs(
        CT_BASE_PATH / cfg["subdir"][:-6], image_ct, image, cfg["alignment"], n_transforms = 10
    )
    time_propagate_dvfs.append(time.time() - start_time)

    # Read respiration trace and compute magnitudes
    resp_trace = np.loadtxt(str(trace_file), delimiter=",", skiprows=1)
    directions = get_trace_direction(resp_trace)
    magn_in, magn_ex, split_idx = assign_magnitude_to_dvfs(
        dvfs_ct, ct_path, resp_trace, dvfs
    )

    # Prepare output directories
    cine_dirs = create_output_dirs(img_dir, case_id, extract_sagittal_coronal)
    
    # Smooth and synthesize cine
    global time_synthesize_cine
    time_synthesize_cine.extend(synthesize_cine(
        dvfs,
        magn_in,
        magn_ex,
        split_idx,
        directions,
        resp_trace,
        segmentation,
        image,
        cine_dirs,
        cfg,
        extract_sagittal_coronal,
        application=APPLICATION
    ))

def load_and_propagate_dvfs(
    ct_dir: Path,
    image_ct: sitk.Image,
    image_mr: sitk.Image,
    alignment: tuple,
    n_transforms: int = 10
):
    """
    Load transforms, convert to displacement fields, resample to MR space.
    """
    dvfs, dvfs_ct = [], []
    rigid = sitk.TranslationTransform(3)
    rigid.SetParameters(alignment)
    tf2disp = sitk.TransformToDisplacementFieldFilter()
    tf2disp.SetReferenceImage(image_ct)

    for idx in range(n_transforms):
        tx_file = ct_dir / "DVFReverse" / f"dvfReverse{idx}.hdf5"
        tx = sitk.ReadTransform(str(tx_file))
        disp_ct = tf2disp.Execute(tx)
        dvfs_ct.append(sitk.Resample(disp_ct, image_ct)) # For Jacobian later
        disp_mr = sitk.Resample(disp_ct, image_mr, rigid.GetInverse()) # Resample the displacement field into MR image space using inverse rigid transform
        mask = sitk.Resample(disp_ct, image_mr, rigid.GetInverse(), sitk.sitkNearestNeighbor, defaultPixelValue=999.0 )
        disp_mr = propagate_dvf(4, disp_mr, mask)
        dvfs.append(disp_mr)
        del disp_mr, mask
    del disp_ct, tx_file, tx
    gc.collect()
    return dvfs, dvfs_ct

if __name__ == "__main__":
    if APPLICATION == "A_4D_CT":
        cases = A_4D_CT_CASES
    elif APPLICATION == "B_4D_MR":
        cases = B_4D_MR_CASES
    else: 
        cases = C_4D_MR_CASES
        
    for cid in range(1, 21):
        time_propagate_dvfs = []
        time_synthesize_cine = []
        process_case(cid)

        desktop = Path.home() / "Desktop"
        file_path = desktop / "stats_create4D.csv"
        if not file_path.exists():
            file_path.touch()
            
        # Compute average values
        avg_dvfs = sum(time_propagate_dvfs) / len(time_propagate_dvfs)
        avg_cine = sum(time_synthesize_cine) / len(time_synthesize_cine)
    
        # Append the info to the file
        with open(file_path, "a") as f:
            f.write(f"{APPLICATION},{cid}, avg time to propagate a DVF, {avg_dvfs}\n")
            f.write(f"{APPLICATION},{cid}, avg time to generate a 3D cine image, {avg_cine}\n")
            print("Processing complete.\n")
  


"""
Reorient medical images to LPS space (orthogonal).

This script can process a directory of medical images (NIfTI `.nii.gz`, `.mha`, etc.),
reorienting each file to LPS space. Segmentation images are resampled with nearest-neighbor
interpolation, while intensity images use linear interpolation.
"""

import os
import SimpleITK as sitk
from pathlib import Path

APPLICATION = 'C_4D_MR' # 'A_4D_CT', 'B_4D_MR', 'C_4D_MR'
 
def force_orthogonal_to_LPS(image, is_label = False):
    """
    Force reorientation to LPS space even for oblique images.
    """
    
    # Get original spacing, size, and origin
    spacing = image.GetSpacing()
    size = image.GetSize()
    origin = image.GetOrigin()
    
    # Define identity direction for LPS
    lps_direction = (1.0, 0.0, 0.0,
                     0.0, 1.0, 0.0,
                     0.0, 0.0, 1.0)
    
    # Create reference image in LPS
    reference = sitk.Image(size, image.GetPixelID())
    reference.SetSpacing(spacing)
    reference.SetOrigin(origin)
    reference.SetDirection(lps_direction)
    
    # Resample to this reference image
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(reference)
    resampler.SetInterpolator(sitk.sitkNearestNeighbor if is_label else sitk.sitkLinear)
    resampler.SetDefaultPixelValue(0)
    
    reoriented = resampler.Execute(image)
    return reoriented


for case_id in range(1,21):
    
    path_images = Path(__file__).resolve().parent / APPLICATION / f"Data{case_id}/"
        
    for filename in os.listdir(path_images):
        if filename[-3:] == 'mha' or filename[-6:] == 'nii.gz':
            image = sitk.ReadImage(os.path.join(path_images, filename))
            lps_image = sitk.DICOMOrient(image, 'LPS')
            is_label = "segmentation" in filename.lower()
            orthogonal_image = force_orthogonal_to_LPS(lps_image, is_label)
            sitk.WriteImage(orthogonal_image, os.path.join(path_images, filename))

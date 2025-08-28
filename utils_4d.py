"""
Utility functions for anatomical orientation, DVF propagation,
respiratory phase computation, and DVF interpolation.
"""
import gc
from pathlib import Path
import time

import numpy as np
import SimpleITK as sitk
import cv2
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter

def get_anatomical_orientation(image: sitk.Image) -> str:
    """
    Return LPS-based anatomical orientation for an image.

    Uses direction cosines to determine dominant axis orientations.
    """
    direction = image.GetDirection()
    labels = ['L', 'P', 'S', 'R', 'A', 'I']
    orientation = []

    for axis in range(3):
        vec = direction[axis::3]
        idx = int(np.argmax(np.abs(vec)))
        sign_offset = 3 if vec[idx] < 0 else 0
        orientation.append(labels[idx + sign_offset])

    return ''.join(orientation)


def force_orthogonal(
    target: sitk.Image, reference: sitk.Image, is_label: bool = False
) -> sitk.Image:
    """
    Resample target image to match reference grid and orientation.

    Parameters:
        target: source image (may be oblique)
        reference: orthogonal reference image
        is_label: use nearest-neighbor for labels, linear for images
    """
    min_value = sitk.GetArrayViewFromImage(target).min()
    reference_img = sitk.Image(target.GetSize(), target.GetPixelID())
    reference_img.SetSpacing(target.GetSpacing())
    reference_img.SetOrigin(target.GetOrigin())
    reference_img.SetDirection(reference.GetDirection())

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(reference_img)
    interp = sitk.sitkNearestNeighbor if is_label else sitk.sitkLinear
    resampler.SetInterpolator(interp)
    resampler.SetDefaultPixelValue(float(min_value))

    return resampler.Execute(target)


def propagate_dvf(
    inpaint_radius: int,
    dvf_image: sitk.Image,
    mask_image: sitk.Image,
) -> sitk.Image:
    """
    Inpaint and smooth DVF regions where displacement is undefined.

    - Uses OpenCV inpainting per slice
    - Applies exponential decay based on distance map
    """
    spacing = dvf_image.GetSpacing()
    # Extract zero mask and prepare arrays
    mask_arr = (sitk.GetArrayFromImage(mask_image) == 999.0).astype(np.uint8)
    mask_bin = mask_arr[..., 0]
    dvf_arr = sitk.GetArrayFromImage(dvf_image)
    inpainted = np.zeros_like(dvf_arr)

    for vec_comp in range(3):
        vec_comp_slices = dvf_arr[..., vec_comp]
        for y in range(vec_comp_slices.shape[1]):
            slice_img = vec_comp_slices[:, y, :].astype(np.float32)
            mask_slice = mask_bin[:, y, :] * 255                

            # Normalize to 0-255 for inpainting
            minv, maxv = slice_img.min(), slice_img.max()
            scale = (maxv - minv) if maxv != minv else 1
            norm = ((slice_img - minv) / scale * 255).astype(np.uint8)

            inp = cv2.inpaint(norm, mask_slice, inpaint_radius, cv2.INPAINT_NS)
            restored = (inp.astype(np.float32) / 255 * scale + minv)
            
            # Find 255→0 transition rows
            transition_rows = np.where((mask_slice[:-1] > 200) & (mask_slice[1:] < 50))[0] + 1

            # Step 6: Zero out first 4 transition rows (clip to max row index)
            if transition_rows.size:
                for r in range(transition_rows[0]-4, transition_rows[0]+4):
                    if r < mask_slice.shape[0] and r>0:
                        mask_slice[r, :] = 255   

            # Decay map in mm
            mask_itk = sitk.GetImageFromArray(mask_slice.astype(np.uint8))
            mask_itk.SetSpacing((spacing[0], spacing[2]))
            dist_map = sitk.GetArrayFromImage(
                sitk.SignedMaurerDistanceMap(
                    mask_itk,
                    insideIsPositive=True,
                    squaredDistance=False,
                    useImageSpacing=True
                )
            )
            
            m, s = 200, 40
            decay = 1 / (1 + np.exp((np.clip(dist_map, 0, None) - m) / s))
            decay[dist_map <= 0] = 1.0
            inpainted[..., vec_comp][:, y, :] = np.where(mask_slice > 0, restored * decay, slice_img)

    sigmas = (1, 1, 1, 0.0)
    smoothed = gaussian_filter(inpainted, sigma=sigmas)
    inpainted = np.where(mask_arr, smoothed, inpainted)
    out_img = sitk.GetImageFromArray(inpainted, isVector=True)
    out_img.CopyInformation(dvf_image)
    gc.collect()
    return out_img


def get_trace_direction(
    resp_trace: np.ndarray
) -> tuple[int, int, int, int, np.ndarray]:
    """
    Compute respiratory phase direction.

    Returns:
        direction_array
    """
    velocity = np.gradient(resp_trace[:, 2])
    smoothed = savgol_filter(velocity, window_length=7, polyorder=2)
    direction = np.where(smoothed >= 0, 1, -1)

    # Remove spurious flips
    for _ in range(2):
        flips = np.where(np.diff(direction) != 0)[0]
        for idx in flips:
            if 0 < idx < len(direction) - 1:
                direction[idx] = direction[idx - 1]
    gc.collect()
    return direction


def assign_magnitude_to_dvfs(
    dvfs_ct: list[sitk.Image],
    ct_path: Path,
    resp_trace: np.ndarray,
    dvfs_mr: list[sitk.Image]
) -> tuple[np.ndarray, np.ndarray, int]:
    """
    Assign respiratory magnitudes to inhale and exhale DVF frames by sampling
    evenly over the corresponding portions of the respiratory trace.

    Returns:
        mags_inhale: magnitudes for inhale frames
        mags_exhale: magnitudes for exhale frames
        split_index: index separating inhale/exhale in dvfs_ct
        dvfs_mr: reordered dvfs_mr matching split
    """
    # Attempt Jacobian-based split
    split_idx = len(dvfs_ct) // 2 # Default midpoint split
    
    seg_dir = ct_path.parent.parent / 'Segmentations'
    if seg_dir.exists():
        lung_files = list(seg_dir.glob('*[LlrR]ung*.nii*'))
        if lung_files:  # Use Jacobian determinant for smarter splitting if possible
            roi_jac = []
            for dvf in dvfs_ct:
                jac = sitk.DisplacementFieldJacobianDeterminant(dvf)
                jac_arr = sitk.GetArrayFromImage(jac)
                mask = sitk.GetArrayFromImage(sitk.ReadImage(str(lung_files[0]), sitk.sitkUInt8))
                roi_jac.append(jac_arr[mask == 1].mean())
            vel = np.gradient(roi_jac)
            sm = savgol_filter(vel, window_length=3, polyorder=2)
            phases = np.where(sm >= 0, 1, -1)
            changes = np.where(np.diff(phases) != 0)[0] + 1
            if changes.size:
                split_idx = int(min(changes, key=lambda x: abs(x-split_idx)))

        # Evenly assign magnitudes
        min_res, max_res = float(np.min(resp_trace[:, 2])), float(np.max(resp_trace[:, 2]))
    
        mags_in = np.linspace(min_res, max_res, split_idx) 
        mags_ex = np.linspace(max_res, min_res, len(dvfs_ct)-split_idx)

        return mags_in, mags_ex, split_idx


def get_blend_weights_unsorted(
    ref_mags: np.ndarray,
    target_mag: float,
    phase: int
) -> tuple[int, int, float, float]:
    """
    Compute low/high indices and weights for linear interpolation of DVFs.
    """
    diffs = ref_mags - target_mag
    below = diffs < 0
    above = diffs >= 0

    if not below.any() or not above.any(): 
        idx = int(np.argmin(np.abs(diffs)))
        return idx, idx,target_mag/(2*ref_mags[idx]), target_mag/(2*ref_mags[idx])
    
    below = list(below)
    switch_indices  = [i for i in range(1, len(below)) if below[i] != below[i-1]]
    idx_high = switch_indices[0]
    idx_low = idx_high -1
    low, high = ref_mags[idx_low], ref_mags[idx_high]
    w_high = (target_mag - low) / (high - low)
    w_low = 1 - w_high
    gc.collect()
    return idx_low, idx_high, w_low, w_high


def interpolate_dvfs_directional(
    dvfs: list[sitk.Image],
    mags_in: np.ndarray,
    mags_ex: np.ndarray,
    target_mag: float,
    phase: int,
    split_idx: int = 5
) -> sitk.Image:
    """
    Interpolate DVFs based on respiratory phase and magnitude.
    """
    if phase == 1:
        ref, mags = dvfs[:split_idx], mags_in 
    else:
        ref, mags = dvfs[split_idx:], mags_ex 

    low, high, w_low, w_high = get_blend_weights_unsorted(mags, target_mag, phase)
    comps_low = [sitk.VectorIndexSelectionCast(ref[low], i) for i in range(3)]
    comps_high = [sitk.VectorIndexSelectionCast(ref[high], i) for i in range(3)]
    blended = [sitk.Add(l*w_low, h*w_high) for l, h in zip(comps_low, comps_high)]
    out = sitk.Compose(blended)
    gc.collect()
    return out


def moving_average_dvfs(dvfs: list[sitk.Image]) -> sitk.Image:
    """
    Compute element-wise average of a list of DVF images.
    """
    n = len(dvfs)
    added_components = [sitk.VectorIndexSelectionCast(dvfs[0], i)*(1/len(dvfs)) for i in range(3)]
    for d_ind in range(1, n):
        d_components = [sitk.VectorIndexSelectionCast(dvfs[d_ind], i)*(1/len(dvfs)) for i in range(3)]
        added_components = [sitk.Add(d, m) for d, m in zip(added_components, d_components)]
    out = sitk.Compose(added_components) # Compose them back into a vector image
    del dvfs
    gc.collect()
    return out

def reorient_and_resample(image: sitk.Image, reference: sitk.Image, is_label: bool):
    """
    Ensure image has the same orientation and grid as reference.
    """
    if get_anatomical_orientation(image) != get_anatomical_orientation(reference):
        image = sitk.DICOMOrient(image, get_anatomical_orientation(reference))
    image = force_orthogonal(image, reference, is_label=is_label)
    return image

def load_and_prepare_img_seg(mr_dir: Path, image_ct: sitk.Image, APPLICATION: str):
    """
    Load MR volume and segmentation, reorient and resample to CT.
    """
    image, segmentation = None, None
    for file in mr_dir.iterdir():
        name = file.name
        if name.startswith("VolumeCine") or name.startswith("Image"):
            if 'CT' in APPLICATION:
                image = sitk.ReadImage(str(file), sitk.sitkInt32)
            else:
                image = sitk.ReadImage(str(file), sitk.sitkFloat32)
            image = reorient_and_resample(image, image_ct, is_label=False)
            sitk.WriteImage(image, str(file))  # overwrite in place
        elif name.startswith("SegmentationCine"):
            segmentation = sitk.ReadImage(str(file), sitk.sitkUInt8)
            segmentation = reorient_and_resample(segmentation, image_ct, is_label=True)
            sitk.WriteImage(segmentation, str(file))  # overwrite in place
        if image and segmentation:
            break
    return image, segmentation

def extract_slices(image: sitk.Image, cfg: dict) -> dict:
    """
    Useful only if users wants to extract coronal and sagittal images from synthetic 3D images.
    """
    # Full volume size
    cor_size, sag_size = list(image.GetSize()), list(image.GetSize())
    cor_idx, sag_idx = [0, cfg["coronal_idx"], 0], [cfg["sagittal_idx"], 0, 0]  #all images are RAI or LPS

    # Coronal
    cor_size[1] = 1
    cor_slice = sitk.DICOMOrient(sitk.Extract(image, size=cor_size, index=cor_idx), 'LIP')

    # Sagittal
    sag_size[0] = 1
    sag_slice = sitk.DICOMOrient(sitk.Extract(image, size=sag_size, index=sag_idx), 'PIR')

    return {"coronal": cor_slice, "sagittal": sag_slice}

def synthesize_cine(
    dvfs,
    magnitudes_inhale,
    magnitudes_exhale,
    split_idx,
    directions,
    resp_trace,
    segmentation,
    image,
    cine_dirs,
    cfg,
    extract_sagittal_coronal,
    application
):
    """
    Generate temporally-smoothed DVFs and apply to produce cine frames.
    """
    buffer, counter, window, time_synthesize_3D_cine = [], 0, 4, []
    if extract_sagittal_coronal == True:
        slices = extract_slices(image, cfg)
        use_sagittal = True

    for t, phase in enumerate(directions):
        start_time = time.time()
        synthetic = interpolate_dvfs_directional(
            dvfs, magnitudes_inhale, magnitudes_exhale, resp_trace[t, 2], phase, split_idx
        )
        buffer.append(synthetic)

        if len(buffer) == window:
            smooth = moving_average_dvfs(buffer)
            ### Uncomment if user wants to save the applied DVF
            # sitk.WriteImage(sitk.Cast(smooth, sitk.sitkVectorFloat32), str(cine_dirs["CineDVFs"] / f"dvf{counter:03d}.nii.gz"))
            transform = sitk.DisplacementFieldTransform(smooth)

            # 3D cine
            min_value = sitk.GetArrayViewFromImage(image).min()
            img3d = sitk.Resample(image, image, transform, defaultPixelValue = float(min_value))
            time_synthesize_3D_cine.append(time.time() - start_time)
            seg3d = sitk.Resample(segmentation, segmentation, transform, sitk.sitkNearestNeighbor)
            sitk.WriteImage(img3d, str(cine_dirs["Cine3D"] / f"image{counter:03d}.nii.gz"))
            sitk.WriteImage(seg3d, str(cine_dirs["Cine3DSegmentations"] / f"seg{counter:03d}.nii.gz"))

            ## If user wants to extract 2D sagittal and coronal images
            if extract_sagittal_coronal == True:
                slice_key = "sagittal" if use_sagittal else "coronal"
                sl = slices[slice_key]
                img2d = sitk.Resample(image, sl, transform, defaultPixelValue = float(min_value))
                seg2d = sitk.Resample(segmentation, sl, transform, sitk.sitkNearestNeighbor)
                sitk.WriteImage(img2d, str(cine_dirs["Cine2D"] / f"image{counter:03d}.nii.gz"))
                sitk.WriteImage(seg2d, str(cine_dirs["Cine2DSegmentations"] / f"seg{counter:03d}.nii.gz"))
                use_sagittal = not use_sagittal

            buffer.pop(0)
            counter += 1
            if counter >= 600: # Modify to number of images required
                break

    gc.collect()
    return time_synthesize_3D_cine
    
def create_output_dirs(base_dir: Path, case_id: int, extract_sagittal_coronal: bool) -> dict:
    """
    Create and return dictionary of output directories for cine images, segmentations, and DVFs.
    """
    key = f"Data{case_id}"
    dirs = {}
    for suffix in ["Cine3D", "Cine3DSegmentations"]: # Add "CineDVFs" to the list and uncomment line 343 if user wants to save GT DVFs 
        path = base_dir / f"{key}{suffix}"
        path.mkdir(parents=True, exist_ok=True)
        dirs[suffix] = path
    if extract_sagittal_coronal == True:
        for suffix in ["Cine2D", "Cine2DSegmentations"]:
            path = base_dir / f"{key}{suffix}"
            path.mkdir(parents=True, exist_ok=True)
            dirs[suffix] = path
    return dirs
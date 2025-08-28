# config_ct.py
from pathlib import Path

# Base folder for all CT cases
CT_BASE_PATH = Path(__file__).resolve().parent / "Source_4D_Lung"

# Per-case settings
A_4D_CT_CASES = {
    1: {
        "subdir": "100_HM10395_07-02-2003-NA-p4-14571/3DCine", 
        "file": "Image00000.nii.gz", 
        "coronal_idx": 257, 
        "sagittal_idx": 196, 
        "alignment": (0, 0, 0)
        },
    2: {
        "subdir": "101_HM10395_10-21-1997-NA-p4-86157/3DCine", 
        "file": "Image00010.nii.gz", 
        "coronal_idx": 316, 
        "sagittal_idx": 208, 
        "alignment": (0, 0, 0)
        },
    3: {
        "subdir": "102_HM10395_03-25-1998-NA-p4-57341/3DCine", 
        "file": "Image00020.nii.gz", 
        "coronal_idx": 320, 
        "sagittal_idx": 182, 
        "alignment": (0, 0, 0)
        },
    4: {
        "subdir": "103_HM10395_06-17-1998-NA-p4-43192/3DCine", 
        "file": "Image00030.nii.gz", 
        "coronal_idx": 310, 
        "sagittal_idx": 177, 
        "alignment": (0, 0, 0)
        },
    5: {
        "subdir": "104_HM10395_09-29-1998-NA-p4-84934/3DCine", 
        "file": "Image00040.nii.gz", 
        "coronal_idx": 257, 
        "sagittal_idx": 195, 
        "alignment": (0, 0, 0)
        },
    6: {
        "subdir": "106_HM10395_10-08-1998-NA-p4-53394/3DCine", 
        "file": "Image00060.nii.gz", 
        "coronal_idx": 297, 
        "sagittal_idx": 190, 
        "alignment": (0, 0, 0)
        },
    7: {
        "subdir": "107_HM10395_06-02-1999-NA-p4-89680/3DCine", 
        "file": "Image00080.nii.gz", 
        "coronal_idx": 273, 
        "sagittal_idx": 190, 
        "alignment": (0, 0, 0)
        },
    8: {
        "subdir": "107_HM10395_06-09-1999-NA-p4-63882/3DCine", 
        "file": "Image00090.nii.gz", 
        "coronal_idx": 300, 
        "sagittal_idx": 201, 
        "alignment": (0, 0, 0)
        },
    9: {
        "subdir": "109_HM10395_11-19-1999-NA-p4-97769/3DCine",
        "file": "Image00070.nii.gz",
        "coronal_idx": 315,
        "sagittal_idx": 191,
        "alignment": (0, 0, 0)
        },
    10: {
        "subdir": "108_HM10395_07-28-1999-NA-p4-56648/3DCine", 
        "file": "Image00030.nii.gz", 
        "coronal_idx": 282, 
        "sagittal_idx": 178, 
        "alignment": (0, 0, 0)
        },
    11: {
        "subdir": "109_HM10395_10-22-1999-NA-p4-18291/3DCine", 
        "file": "Image00040.nii.gz", 
        "coronal_idx": 261, 
        "sagittal_idx": 175, 
        "alignment": (0, 0, 0)
        },
    12: {
        "subdir": "111_HM10395_11-03-1999-NA-p4-34158/3DCine", 
        "file": "Image00270.nii.gz", 
        "coronal_idx": 323, 
        "sagittal_idx": 344, 
        "alignment": (0, 0, 0)
        },
    13: {
        "subdir": "111_HM10395_12-01-1999-NA-p4-78209/3DCine", 
        "file": "Image00110.nii.gz", 
        "coronal_idx": 282, 
        "sagittal_idx": 172, 
        "alignment": (0, 0, 0)
        },
    14: {
        "subdir": "112_HM10395_10-20-1999-NA-p4-34722/3DCine",
        "file": "Image00310.nii.gz",
        "coronal_idx": 294, 
        "sagittal_idx": 187, 
        "alignment": (0, 0, 0)
        },
    15: {
        "subdir": "119_HM10395_01-08-2001-NA-p4-95100/3DCine", 
        "file": "Image00730.nii.gz", 
        "coronal_idx": 302, 
        "sagittal_idx": 193, 
        "alignment": (0, 0, 0)
        },
    16: {
        "subdir": "113_HM10395_12-03-1999-NA-p4-12989/3DCine", 
        "file": "Image00200.nii.gz", 
        "coronal_idx": 295, 
        "sagittal_idx": 206, 
        "alignment": (0, 0, 0)
        },
    17: {
        "subdir": "114_HM10395_04-21-2000-NA-p4-11761/3DCine", 
        "file": "Image00240.nii.gz", 
        "coronal_idx": 257, 
        "sagittal_idx": 172, 
        "alignment": (0, 0, 0)
        },
    18: {
        "subdir": "115_HM10395_04-26-2000-NA-p4-06742/3DCine", 
        "file": "Image00470.nii.gz", 
        "coronal_idx": 307, 
        "sagittal_idx": 185, 
        "alignment": (0, 0, 0)
        },
    19: {
        "subdir": "117_HM10395_11-17-2000-NA-p4-43681/3DCine", 
        "file": "Image00360.nii.gz", 
        "coronal_idx": 257, 
        "sagittal_idx": 175, 
        "alignment": (0, 0, 0)
        },
    20: {
        "subdir": "118_HM10395_12-07-2000-NA-p4-71576/3DCine", 
        "file": "Image00700.nii.gz", 
        "coronal_idx": 312, 
        "sagittal_idx": 203, 
        "alignment": (0, 0, 0)
        },
}

B_4D_MR_CASES = {
    1: {
        "subdir": "109_HM10395_10-22-1999-NA-p4-18291/3DCine",
        "file": "Image00040.nii.gz",
        "coronal_idx": 153,
        "sagittal_idx": 96,
        "alignment": (-5.5, -26.7, 164.2),
    },
    2: {
        "subdir": "101_HM10395_10-21-1997-NA-p4-86157/3DCine",
        "file": "Image00010.nii.gz",
        "coronal_idx": 216,
        "sagittal_idx": 114,
        "alignment": (0.4, 26.0, 139.0),
    },
    3: {
        "subdir": "102_HM10395_03-25-1998-NA-p4-57341/3DCine",
        "file": "Image00020.nii.gz",
        "coronal_idx": 134,
        "sagittal_idx": 82,
        "alignment": (7.0, 2.0, 262.0),
    },
    4: {
        "subdir": "119_HM10395_01-08-2001-NA-p4-95100/3DCine",
        "file": "Image00730.nii.gz",
        "coronal_idx": 109,
        "sagittal_idx": 56,
        "alignment": (-11, 17, 223),
    },
    5: {
        "subdir": "104_HM10395_09-29-1998-NA-p4-84934/3DCine",
        "file": "Image00040.nii.gz",
        "coronal_idx": 151,
        "sagittal_idx": 121,
        "alignment": (9, 0, 200),
    },
    6: {
        "subdir": "114_HM10395_05-05-2000-NA-p4-38187/3DCine",
        "file": "Image00260.nii.gz",
        "coronal_idx": 123,
        "sagittal_idx": 104,
        "alignment": (-24.0, -28.0, 117.0),
    },
    7: {
        "subdir": "106_HM10395_10-08-1998-NA-p4-53394/3DCine",
        "file": "Image00060.nii.gz",
        "coronal_idx": 113,
        "sagittal_idx": 56,
        "alignment": (39.0, 0.3, 185.2),
    },
    8: {
        "subdir": "117_HM10395_11-17-2000-NA-p4-43681/3DCine",
        "file": "Image00360.nii.gz",
        "coronal_idx": 162,
        "sagittal_idx": 88,
        "alignment": (-37.0, 5.0, 124.7),
    },
    9: {
        "subdir": "118_HM10395_12-07-2000-NA-p4-71576/3DCine",
        "file": "Image00700.nii.gz",
        "coronal_idx": 273,
        "sagittal_idx": 156,
        "alignment": (20, 9.5, 112),
    },
    10: {
        "subdir": "107_HM10395_06-09-1999-NA-p4-63882/3DCine",
        "file": "Image00090.nii.gz",
        "coronal_idx": 158,
        "sagittal_idx": 99,
        "alignment": (-22.6, 7.0, 240.0),
    },
    11: {
        "subdir": "113_HM10395_12-03-1999-NA-p4-12989/3DCine",
        "file": "Image00200.nii.gz",
        "coronal_idx": 283,
        "sagittal_idx": 194,
        "alignment": (-12.9, -5.0, 114.0),
    },
    12: {
        "subdir": "112_HM10395_11-26-1999-NA-p4-84295/3DCine",
        "file": "Image00140.nii.gz",
        "coronal_idx": 146,
        "sagittal_idx": 93,
        "alignment": (-25.4, 31.0, 136.0),
    },
    13: {
        "subdir": "108_HM10395_07-28-1999-NA-p4-56648/3DCine",
        "file": "Image00030.nii.gz",
        "coronal_idx": 127,
        "sagittal_idx": 160,
        "alignment": (12.0, 12.0, 265.0),
    },
    14: {
        "subdir": "112_HM10395_12-03-1999-NA-p4-88085/3DCine",
        "file": "Image00150.nii.gz",
        "coronal_idx": 105,
        "sagittal_idx": 71,
        "alignment": (19.2, 5.0, 305.0),
    },
    15: {
        "subdir": "103_HM10395_06-17-1998-NA-p4-43192/3DCine",
        "file": "Image00030.nii.gz",
        "coronal_idx": 127,
        "sagittal_idx": 96,
        "alignment": (-2, 41, 145),
    },
    16: {
        "subdir": "111_HM10395_11-03-1999-NA-p4-34158/3DCine",
        "file": "Image00270.nii.gz",
        "coronal_idx": 93,
        "sagittal_idx": 80,
        "alignment": (9.0, -26.0, 197.7),
    },
    17: {
        "subdir": "112_HM10395_10-20-1999-NA-p4-34722/3DCine",
        "file": "Image00310.nii.gz",
        "coronal_idx": 153,
        "sagittal_idx": 99,
        "alignment": (-9, 31, 280),
    },
    18: {
        "subdir": "114_HM10395_04-21-2000-NA-p4-11761/3DCine",
        "file": "Image00240.nii.gz",
        "coronal_idx": 266,
        "sagittal_idx": 154,
        "alignment": (7.0, -10.4, 190.0),
    },
    19: {
        "subdir": "115_HM10395_04-26-2000-NA-p4-06742/3DCine",
        "file": "Image00470.nii.gz",
        "coronal_idx": 120,
        "sagittal_idx": 152,
        "alignment": (-30.0, 19.0, 148.0),
    },
    20: {
        "subdir": "112_HM10395_12-23-1999-NA-p4-79057/3DCine",
        "file": "Image00180.nii.gz",
        "coronal_idx": 250,
        "sagittal_idx": 180,
        "alignment": (13.0, 28.0, 230.0),
    },
}

C_4D_MR_CASES = {
    1: {
        "subdir": "107_HM10395_06-09-1999-NA-p4-63882/3DCine",
        "file": "Image00090.nii.gz",
        "coronal_idx": 63,
        "sagittal_idx": 94,
        "alignment": (-4, -26, 243),
    },
    2: {
        "subdir": "117_HM10395_11-17-2000-NA-p4-43681/3DCine",
        "file": "Image00360.nii.gz",
        "coronal_idx": 61,
        "sagittal_idx": 124,
        "alignment": (-27.0, -6, 113),
    },
    3: {
        "subdir": "112_HM10395_11-26-1999-NA-p4-84295/3DCine",
        "file": "Image00140.nii.gz",
        "coronal_idx": 100,
        "sagittal_idx": 129,
        "alignment": (9, 16.5, 233),
    },
    4: {
        "subdir": "111_HM10395_12-01-1999-NA-p4-78209/3DCine",
        "file": "Image00110.nii.gz",
        "coronal_idx": 245,
        "sagittal_idx": 148,
        "alignment": (41.5, -9, 164),
    },
    5: {
        "subdir": "103_HM10395_06-17-1998-NA-p4-43192/3DCine",
        "file": "Image00030.nii.gz",
        "coronal_idx": 326,
        "sagittal_idx": 196,
        "alignment": (0, 12, 213),
    },
    6: {
        "subdir": "109_HM10395_10-22-1999-NA-p4-18291/3DCine",
        "file": "Image00040.nii.gz",
        "coronal_idx": 62,
        "sagittal_idx": 112,
        "alignment": (41.0, -10, 161),
    },
    7: {
        "subdir": "119_HM10395_01-08-2001-NA-p4-95100/3DCine", 
        "file": "Image00730.nii.gz", 
        "coronal_idx": 41,
        "sagittal_idx": 107,
        "alignment": (-25, 43, 138),
    },
    8: {
        "subdir": "106_HM10395_10-08-1998-NA-p4-53394/3DCine",
        "file": "Image00060.nii.gz",
        "coronal_idx": 49,
        "sagittal_idx": 90,
        "alignment": (35, 15, 214),
    },
    9: {
        "subdir": "104_HM10395_09-29-1998-NA-p4-84934/3DCine",
        "file": "Image00040.nii.gz",
        "coronal_idx": 146,
        "sagittal_idx": 92,
        "alignment": (8, -9, 195),
    },  
    10: {
        "subdir": "101_HM10395_10-21-1997-NA-p4-86157/3DCine",
        "file": "Image00010.nii.gz",
        "coronal_idx": 31,
        "sagittal_idx": 142,
        "alignment": (-3.0, -16, 205),
    },
    11: {
        "subdir": "112_HM10395_12-03-1999-NA-p4-88085/3DCine",
        "file": "Image00150.nii.gz",
        "coronal_idx": 109,
        "sagittal_idx": 73,
        "alignment": (0, 41, 199),
    },
    12: {
        "subdir": "114_HM10395_04-21-2000-NA-p4-11761/3DCine",
        "file": "Image00240.nii.gz",
        "coronal_idx": 121,
        "sagittal_idx": 101,
        "alignment": (-3, -45, 209),
    },
    13: {
        "subdir": "107_HM10395_06-02-1999-NA-p4-89680/3DCine",
        "file": "Image00080.nii.gz",
        "coronal_idx": 260,
        "sagittal_idx": 117,
        "alignment": (-16, 13, 307),
    },
    14: {
        "subdir": "107_HM10395_06-21-1999-NA-p4-00587/3DCine",
        "file": "Image00100.nii.gz",
        "coronal_idx": 34,
        "sagittal_idx": 100,
        "alignment": (-1, -2, 211),
    },
    15: {
        "subdir": "111_HM10395_11-03-1999-NA-p4-34158/3DCine",
        "file": "Image00270.nii.gz",
        "coronal_idx": 301,
        "sagittal_idx": 171,
        "alignment": (37, -40, 171),
    },
    16: {
        "subdir": "113_HM10395_12-03-1999-NA-p4-12989/3DCine",
        "file": "Image00200.nii.gz",
        "coronal_idx": 124,
        "sagittal_idx": 91,
        "alignment": (-9, -50, 188),
    },
    17: {
        "subdir": "108_HM10395_07-28-1999-NA-p4-56648/3DCine",
        "file": "Image00030.nii.gz",
        "coronal_idx": 45,
        "sagittal_idx": 171,
        "alignment": (-2, 30, 180),
    },
    18: {
        "subdir": "117_HM10395_11-21-2000-NA-p4-79553/3DCine",
        "file": "Image00370.nii.gz",
        "coronal_idx": 18,
        "sagittal_idx": 80,
        "alignment": (-2, -6, 189),
    },
    19: {
        "subdir": "115_HM10395_04-26-2000-NA-p4-06742/3DCine",
        "file": "Image00470.nii.gz",
        "coronal_idx": 210,
        "sagittal_idx": 183,
        "alignment": (-29.0, 27.0, 206.0),
    },
    20: {
        "subdir": "102_HM10395_03-25-1998-NA-p4-57341/3DCine",
        "file": "Image00020.nii.gz",
        "coronal_idx": 135,
        "sagittal_idx": 96,
        "alignment": (-13, -9, 310),
    },
}

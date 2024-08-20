#!/usr/bin/env python3

import numpy as np
import pandas as pd


def zfactor(positive_controls, negative_controls):
    return 1 - (
        3
        * (np.std(positive_controls) + np.std(negative_controls))
        / abs(np.mean(positive_controls - np.mean(negative_controls)))
    )


def minmax_normalization(x, minimum, maximum):
    return ((x - minimum) / (maximum - minimum)) * 100


def max_normalization(x, maximum):
    return (x / maximum) * 100


def background_normalize_zfactor(
    grp: pd.DataFrame, blanks="Medium", negative_controls="Negative Control"
) -> pd.DataFrame:
    """
    This function is supposed to be applied to a grouped DataFrame.
    It does the following operations:
        - Background subtraction by subtracting the mean of the blanks per plate
        - Normalization by applying max-normalization using the 'Negative Controls'
        - Z-Factor calculation using negative controls and blanks

    *`negative_controls` are controls with organism (e.g. bacteria) and medium*
    *and are labeled in the input DataFrame as 'Negative Controls'.*
    *`blanks` are controls with only medium and are labeled*
    *in the input DataFrame as 'Medium'.*
    """
    plate_blanks_mean = grp[grp["ID"] == blanks]["Raw Optical Density"].mean()
    # Subtract background noise:
    grp["Denoised Optical Density"] = grp["Raw Optical Density"] - plate_blanks_mean
    plate_denoised_negative_mean = grp[grp["ID"] == negative_controls][
        "Denoised Optical Density"
    ].mean()
    plate_denoised_blank_mean = grp[grp["ID"] == blanks][
        "Denoised Optical Density"
    ].mean()
    # Normalize:
    grp["Relative Optical Density"] = grp["Denoised Optical Density"].apply(
        lambda x: max_normalization(x, plate_denoised_negative_mean)
    )
    # Z-Factor:
    plate_neg_controls = grp[grp["ID"] == negative_controls]["Raw Optical Density"]
    plate_blank_controls = grp[grp["ID"] == blanks]["Raw Optical Density"]
    grp["Z-Factor"] = zfactor(plate_neg_controls, plate_blank_controls)

    return grp


def preprocess(raw_df: pd.DataFrame, input_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(raw_df, input_df)  # merging reader data and input specifications
    df = (
        df.groupby("Barcode")[df.columns]
        .apply(background_normalize_zfactor)
        .reset_index(drop=True)
    )
    return df.round({
        "Denoised Optical Density": 2,
        "Relative Optical Density": 2,
        "Z-Factor": 2
    })


def get_thresholded_subset(
    df: pd.DataFrame,
    negative_controls: str="Negative Control",
    blanks: str="Medium",
    blankplate_organism: str="Blank",
    threshold=None,
) -> pd.DataFrame:
    """
    Expects a DataFrame with a mic_cutoff column
    """
    # TODO: hardcode less columns

    # Use only substance entries, no controls, no blanks etc.:
    substance_df = df[
        (df["ID"] != blanks)
        & (df["ID"] != negative_controls)
        & (df["Organism"] != blankplate_organism)
    ]
    # Apply threshold:
    if threshold:
        substance_df["Cutoff"] = threshold
    else:
        if "mic_cutoff" not in substance_df:
            raise KeyError("Noo 'mic_cutoff' column in Input.xlsx")
    selection = substance_df[
        substance_df["Relative Optical Density"] < substance_df["Cutoff"]
    ]
    # Apply mean and std in case of replicates:
    result = selection.groupby(["ID", "Organism"], as_index=False).agg(
        {
            "Relative Optical Density": ["mean", "std"],
            "ID": ["first", "count"],
            "Organism": "first",
            "Cutoff": "first",
        }
    )
    result.columns = [
        "Relative Optical Density mean",
        "Relative Optical Density std",
        "ID",
        "Replicates",
        "Organism",
        "Cutoff",
    ]
    return result

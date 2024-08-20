#!/usr/bin/env python3

import numpy as np
import pandas as pd
import string


def get_rows_cols(platetype: int) -> tuple[int, int]:
    """
    Obtain number of rows and columns as tuple for corresponding plate type.
    """
    match platetype:
        case 96:
            return 8, 12
        case 384:
            return 16, 24
        case _:
            raise ValueError("Not a valid plate type")


def generate_inputtable(readout_df = None, platetype: int = 384):
    """
    Generates an input table for the corresponding readout dataframe.
    If not readout df is provided, create a minimal input df.
    """
    if readout_df is None:
        barcodes = ["001PrS01001"]
    else:
        barcodes = readout_df["Barcode"].unique()

    substance_df = pd.DataFrame({
        "ID": [f"Substance {i}" for i in range(1, platetype+1)],
        f"Row_{platetype}": [*list(string.ascii_uppercase[:16]) * 24],
        f"Col_{platetype}": sum([[i] * 16 for i in range(1, 24+1)], []),
        "Concentration in mg/mL": 1,
    })
    layout_df = pd.DataFrame({
        "Barcode": barcodes,
        "Replicate": [1] * len(barcodes),
        "Organism": [f"Placeholder Organism {letter}" for letter in string.ascii_uppercase[:len(barcodes)]]
    })
    df = pd.merge(layout_df, substance_df, how="cross")
    return df


def map_96_to_384(
    df_row: pd.Series,
    rowname: str,
    colname: str,
    q_name: str,
) -> tuple[pd.Series, pd.Series]:
    """
    Maps the rows and columns of 4 96-Well plates into a single 384-Well plate.

    Takes row, column and quadrant (each of the 96-well plates is one quadrant) of a well from 4 96-well plates and maps it to the corresponding well in a 384-well plate.
    Returns the 384-Well plate row and column.
    """
    # TODO: Write tests for this mapping function

    row = df_row[rowname]  # 96-well plate row
    col = df_row[colname]  # 96-well plate column
    quadrant = df_row[q_name]  # which of the 4 96-well plate

    rowmapping = dict(
        zip(
            string.ascii_uppercase[0:8],
            np.array_split(list(string.ascii_uppercase)[0:16], 8),
        )
    )
    colmapping = dict(
        zip(list(range(1, 13)), np.array_split(list(range(1, 25)), 12))
    )
    row_384 = rowmapping[row][0 if quadrant in [1, 2] else 1]
    col_384 = colmapping[col][0 if quadrant in [1, 3] else 1]
    return row_384, col_384


def mapapply_96_to_384(
    df: pd.DataFrame,
    rowname: str = "Row_96",
    colname: str = "Column_96",
    q_name: str = "Quadrant",
) -> pd.DataFrame:
    """
    Apply to a DataFrame the mapping of 96-well positions to 384-well positions.
    The DataFrame has to have columns with:
        - 96-well plate row positions
        - 96-well plate column positions
        - 96-well plate to 384-well plate quadrants
        *(4 96-well plates fit into 1 384-well plate)*
    """
    df["Row_384"], df["Col_384"] = zip(
        *df.apply(
            lambda row: map_96_to_384(
                row, rowname=rowname, colname=colname, q_name=q_name
            ),
            axis=1,
        )
    )
    return df


def split_position(
    df: pd.DataFrame,
    position: str = "Position",
    row: str = "Row_384",
    col: str = "Col_384",
) -> pd.DataFrame:
    """
    Split a position like "A1" into row and column positions ("A", 1) and adds them as columns to the DataFrame.
    """
    df[row] = df[position].apply(lambda x: str(x[0]))
    df[col] = df[position].apply(lambda x: str(x[1:]))
    return df


def process_inputfile(file_object):
    """
    Read Input excel file which should have the following columns:
        - Barcode
        - Organism
        - Row_384
        - Col_384
        - ID
    Optional columns:
        - Concentration in mg/mL (or other units)
        - Cutoff
    """
    if not file_object:
        return None
    excel_file = pd.ExcelFile(file_object)
    substance_df = pd.read_excel(excel_file, "substances")
    layout_df = pd.read_excel(excel_file, "layout")
    df = pd.merge(layout_df, substance_df, how="cross")
    # df.rename(columns={
    #     "barcode": "Barcode",
    #     "replicate": "Replicate",
    #     "organism": "Organism",
    #     "plate_row": "Row_384",
    #     "plate_column": "Col_384",
    #     "id": "ID",
    #     "concentration": "Concentration in mg/mL",
    # }, inplace=True)
    df["ID"] = df["ID"].astype(str)
    return df



def get_upsetplot_df(df, set_column="Organism", counts_column="ID"):
    """
    Function to obtain a correctly formatted DataFrame.
    According to [UpSetR-shiny](https://github.com/hms-dbmi/UpSetR-shiny)
    this table is supposed to be encoded in binary and set up so that each column represents a set, and each row represents an element.
    If an element is in the set it is represented as a 1 in that position. If an element is not in the set it is represented as a 0.

    *Thanks to: https://stackoverflow.com/questions/37381862/get-dummies-for-pandas-column-containing-list*
    """
    tmp_df = (
        df
        .groupby(counts_column)[set_column]
        .apply(lambda x: x.unique())
        .reset_index()
    )
    dummies_df = (
        pd.get_dummies(
            tmp_df.join(
                pd.Series(
                    tmp_df[set_column]
                    .apply(pd.Series)
                    .stack()
                    .reset_index(1, drop=True),
                    name=set_column + "1",
                )
            )
            .drop(set_column, axis=1)
            .rename(columns={set_column + "1": set_column}),
            columns=[set_column],
        )
        .groupby(counts_column, as_index=False)
        .sum()
    )
    # remove "{set_column}_" from set column labels
    dummies_df.columns = list(
        map(
            lambda x: "".join(x.split("_")[1:])
            if x.startswith(set_column)
            else x,
            dummies_df.columns,
        )
    )
    # remove any dots as they interfere with altairs plotting.
    dummies_df.columns = dummies_df.columns.str.replace(".", "")
    return dummies_df

"""Functions for collection mapping files conversion (excel to toml, toml to excel)."""

from pathlib import Path
import pandas as pd
from tomlkit import document
from tomlkit import table
from ava_shared_resources import constants as const
from ava_shared_resources.data_io_utils import (
    check_output_directory,
    load_data,
    save_data,
    load_toml,
    save_toml,
)


def excel_to_toml(input_path: Path, output_path: Path):
    """Convert excel file into toml file.

    :param input_path:path to toml file.
    :param output_path:path to save excel file.
    """
    check_output_directory(output_path)

    mapping_df = load_data(input_path)

    config = _excel_to_toml(mapping_df)

    save_toml(config, output_path)


def _excel_to_toml(df: pd.DataFrame):
    """Convert DataFrame into tomlkit TOMLDocument object.

    :param df:Dataframe with collection mappings.
    :return: tomlkit TOMLDocument object with collection mappings
    """
    df[const.EXCEL_FILE_METADATA_COLUMN] = df[
        const.EXCEL_FILE_METADATA_COLUMN
    ].str.split(";")
    df = df.explode(const.EXCEL_FILE_METADATA_COLUMN).reset_index(drop=True)
    df[const.EXCEL_FILE_METADATA_COLUMN] = df[const.EXCEL_FILE_METADATA_COLUMN].apply(
        lambda x: str(x).strip()
    )
    df = df.sort_values(by=[const.EXCEL_FILE_METADATA_COLUMN])

    values = df[const.EXCEL_FILE_METADATA_COLUMN].to_list()
    collections = df[const.EXCEL_FILE_COLLECTION_COLUMN].to_list()

    if len(values) == len(collections):
        mapping_dict = dict(zip(values, collections))
        config = document()
        collections = table()
        for key, val in mapping_dict.items():
            if str(key) != "":
                collections.add(key, val)
                collections[key].trivia.indent = "\t"

        # get default collection
        default = table()
        default.add(const.TOML_FILE_DEFAULT_COLLECTION_KEY, mapping_dict.get("", ""))
        default[const.TOML_FILE_DEFAULT_COLLECTION_KEY].trivia.indent = "\t"

        config.add(const.TOML_FILE_COLLECTION_HEADER, collections)
        config.add(const.TOML_FILE_DEFAULT_HEADER, default)
    else:
        raise ValueError(
            f"{const.EXCEL_FILE_METADATA_COLUMN} and {const.EXCEL_FILE_COLLECTION_COLUMN} column values count mismatch."
            f" {const.EXCEL_FILE_METADATA_COLUMN} column values must be present for every collection "
            f"except for default collection."
        )
    return config


def toml_to_excel(input_path: Path, output_path: Path):
    """Convert toml file into excel file.

    :param input_path:path to toml file.
    :param output_path:path to save excel file.
    """
    check_output_directory(output_path)

    mapping_config = load_toml(input_path)

    df = _toml_to_excel(mapping_config)

    save_data(df, output_path)


def _toml_to_excel(config: dict):
    """Convert dictionary into DataFrame.

    :param config: dictionary containing collection mappings.
    :return: Dataframe with collection mappings
    """
    mapping_dict = dict()
    mapping_dict[const.EXCEL_FILE_METADATA_COLUMN] = list(
        config[const.TOML_FILE_COLLECTION_HEADER].keys()
    )
    mapping_dict[const.EXCEL_FILE_COLLECTION_COLUMN] = list(
        config[const.TOML_FILE_COLLECTION_HEADER].values()
    )

    # set Empty Metadata Value for default collection
    mapping_dict[const.EXCEL_FILE_METADATA_COLUMN].append("")
    mapping_dict[const.EXCEL_FILE_COLLECTION_COLUMN].append(
        config[const.TOML_FILE_DEFAULT_HEADER][const.TOML_FILE_DEFAULT_COLLECTION_KEY]
    )

    mapping_df = pd.DataFrame(mapping_dict)
    mapping_df = (
        mapping_df.fillna("")
        .groupby([const.EXCEL_FILE_COLLECTION_COLUMN])[const.EXCEL_FILE_METADATA_COLUMN]
        .apply(";".join)
        .reset_index()
    )
    mapping_df = mapping_df[
        [const.EXCEL_FILE_METADATA_COLUMN, const.EXCEL_FILE_COLLECTION_COLUMN]
    ].sort_values(by=[const.EXCEL_FILE_METADATA_COLUMN])

    return mapping_df

"""functions for loading and saving data."""

import csv
import gzip
import hashlib
import logging
import pickle
from pathlib import Path
from typing import Optional, Union, List, Any, Dict

import pandas as pd
import tomli
import tomlkit
from pandas import DataFrame
from tomlkit.toml_document import TOMLDocument

BUF_SIZE = 65 * 1024
log = logging.getLogger(__name__)


def extract_folder_names(filesystem_path: Path) -> List[str]:
    """Extract list of folders from filesystem path.

    :param filesystem_path: Input path to the filesystem.
    :return: List of available directories in the filesystem path.
    """
    subdirectories = []
    try:
        if filesystem_path.exists() and filesystem_path.is_dir():
            subdirectories = [
                entry.name for entry in filesystem_path.iterdir() if entry.is_dir()
            ]
    except Exception as e:
        log.error(f"Error accessing filesystem: {e}")

    return subdirectories


def check_output_directory(path: Union[str, Path], directory: bool = False) -> Path:
    """Make sure that directory of the ``path`` exists. If directory doesn't exist creates the directory.

    :param path: path to file
    :param directory: if True, path is a directory
    :return: path
    """
    out_path = Path(path) if isinstance(path, str) else path
    out_dir = out_path if directory else out_path.parent
    log.debug(f"Checking output folder {out_dir}...")
    if not out_dir.exists():
        log.debug(f"Creating output folder {out_dir}...")
        out_dir.mkdir(parents=True, exist_ok=True)
        log.debug(f"Created output folder {out_dir}")
    return out_path


def log_lines_hash(strings: List[str]):
    """Log hash of a list of strings. This helps to track contents and noticing changes.

    :param strings: lines of text.
    """
    h = calculate_lines_hash(strings)
    log.info(f"{h.name} of {len(strings)} UTF-8-encoded lines of text: {h.hexdigest()}")


def log_binary_hash(path: Path):
    """Log hash of a binary file. This helps to track contents and noticing changes.

    :param path: file path.
    """
    h = calculate_binary_hash(path)
    log.info(f"{h.name} of {path}: {h.hexdigest()}")


def calculate_lines_hash(strings: List[str]) -> Any:
    """Return SHA-256 hash of a list of strings.

    :param strings: lines of text.
    :return: SHA-256 hash
    """
    h = hashlib.sha256()
    for s in strings:
        h.update(s.encode("utf-8"))
    return h


def calculate_binary_hash(path: Path) -> Any:
    """Return SHA-256 hash of a binary file.

    :param path: file path.
    :return: SHA-256 hash
    """
    with path.open("rb") as f:
        h = hashlib.sha256()
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            h.update(data)
    return h


def load_lines(
    path: Path, check_empty: bool = False, allow_empty: bool = True
) -> List[str]:
    """Load lines of text from ``path``.

    Supports ``.txt``, ``.txt.gz`` extensions explicitly, uses UTF-8. Everything else being loaded using pickle.
    :param path: path to load lines from.
    :param check_empty: Should we check for empties.
    :param allow_empty: Should we accept empties.
    :return: List of strings
    """
    log.debug(f"Loading strings from: {path}...")
    log_binary_hash(path)
    if path.name.endswith(".txt") or path.name.endswith(".dat"):
        with path.open("rt", encoding="utf-8") as f:
            result = f.read().split("\n")
    elif path.name.endswith(".txt.gz"):
        # text compresses very well
        with gzip.open(path, "rt", encoding="utf-8") as f:
            result = f.read().split("\n")
    else:
        with path.open("rb") as f:
            result = pickle.load(f)
    inspect_empties(result, path, check_empty, allow_empty)
    log.info(f"Loaded strings: {len(result)}")
    log_lines_hash(result)
    return result


def inspect_empties(
    strings: List[str], path: Path, check_empty: bool, allow_empty: bool
):
    """Inspect empties in list of strings. This function raises ValueError in case inspection fails.

    :param strings: list of strings to be checked for emptiness
    :param path: name of file where strings originated from
    :param check_empty: Should we check for empties.
    :param allow_empty: Should we accept empties.
    """
    if check_empty:
        log.debug("Checking for empty strings...")
        empty_count = strings.count("")
        log.debug(f"Found empty lines in {path}: {empty_count}")
        if (not allow_empty) and (empty_count > 0):
            raise ValueError(f"Empties are not allowed in {path}.")


def save_lines(
    strings: List[str], path: Path, check_empty: bool = False, allow_empty: bool = True
):
    """Save lines of text into ``path``.

    Supports ``.txt``, ``.txt.gz`` extensions explicitly, uses UTF-8. Everything else being saved using pickle.
    In case of text files replaces new lines in ``strings`` with spaces.
    :param strings: lines of text to save.
    :param allow_empty: Should we accept empties.
    :param check_empty: Should we check for empties.
    :param path: path to save lines to.
    """
    inspect_empties(strings, path, check_empty, allow_empty)
    if path is not None:
        log.debug(f"Saving {len(strings)} rows of data to {path}...")
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.name.endswith(".txt") or path.name.endswith(".txt.gz"):
            updated_lines = 0
            for i, s in enumerate(strings):
                if s.find("\n") > -1:
                    strings[i] = s.replace("\n", " ")
                    updated_lines = updated_lines + 1
            if updated_lines > 0:
                log.warning(f"Replaced new lines with spaces in lines: {updated_lines}")

        log.debug(f"Saving strings to {path}...")
        # this makes it easier to debug the pipeline. it is also smaller than pickle.
        if path.name.endswith(".txt") or path.name.endswith(".dat"):
            with path.open("wt", encoding="utf-8") as f:
                f.write("\n".join(strings))
        elif path.name.endswith(".txt.gz"):
            # text compresses very well
            with gzip.open(path, "wt", encoding="utf-8") as f:
                f.write("\n".join(strings))
        else:
            # legacy compatibility
            with path.open("wb") as f:
                pickle.dump(strings, f)
        log_lines_hash(strings)
        log_binary_hash(path)
        log.info(f"Saved strings to {path}")


def load_data(path: Path) -> DataFrame:
    """Load data from a file into data frame.

    Supports .pkl, .tsv, .csv, .xlsx format by respective extensions.
    :param path: path to a file
    :return: data frame with loaded data.
    """
    log.debug(f"Loading data from {path}...")
    log_binary_hash(path)
    if path.name.endswith(".pkl"):
        with path.open("rb") as f:
            df = pickle.load(f)
    elif path.name.endswith(".xlsx") or path.name.endswith(".xls"):
        df = pd.read_excel(path, na_filter=False)
    elif path.name.endswith(".csv") or path.name.endswith(".csv.gz"):
        df = pd.read_csv(path, na_filter=False, encoding="utf-8")
    elif path.name.endswith(".tsv") or path.name.endswith(".tsv.gz"):
        df = pd.read_csv(
            path, sep="\t", na_filter=False, encoding="utf-8", quoting=csv.QUOTE_NONE
        )
    else:
        raise ValueError(f"Unsupported input format: {path.name}")
    log.info(f"Loaded data rows: {len(df)}")
    return df


def save_data(df: DataFrame, path: Optional[Path] = None):
    """Save data frame into a file.

    Supports .pkl, .tsv, .csv, .xlsx format by respective extensions.
    :param df: data frame with data to be saved.
    :param path: path to a file
    """
    if path is not None:
        log.debug(f"Saving {len(df)} rows of data to {path}...")
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.name.endswith(".pkl"):
            with path.open("wb") as f:
                pickle.dump(df, f)
        elif path.name.endswith(".tsv") or path.name.endswith(".tsv.gz"):
            # csv.QUOTE_NONE to force breaking on things that should not be there in the first place
            df.to_csv(
                path, sep="\t", encoding="utf-8", index=False, quoting=csv.QUOTE_NONE
            )
        elif path.name.endswith(".csv") or path.name.endswith(".csv.gz"):
            df.to_csv(path, encoding="utf-8", index=False)
        elif path.name.endswith(".xlsx"):
            df.to_excel(path, engine="openpyxl", index=False)
        else:
            raise ValueError(f"Unsupported format: {path.name}")
        log.info(f"Saved data to {path}")
        log_binary_hash(path)


def replace_none_with_null(data: Union[dict, list]):
    """Replace the string value "None" to the None.

    :param data: dictionary or list for processing
    :return: processed dictionary or list
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if value == "None":
                data[key] = None
            elif isinstance(value, dict) or isinstance(value, list):
                replace_none_with_null(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if item == "None":
                data[i] = None
            elif isinstance(item, dict) or isinstance(item, list):
                replace_none_with_null(item)


def load_toml(path: Path) -> dict:
    """Load data from toml file into data frame.

    Read toml file, parse it and replace string "None" with None value. it is required due to toml doesn't support
    the None (or null) value.
    :param path: path to the file
    :return: parsed content
    """
    log.debug(f"Loading data from {path}...")
    if path.name.endswith(".toml"):
        with open(path, mode="rb") as f:
            data = tomli.load(f)

        replace_none_with_null(data)
    else:
        raise ValueError(f"Unsupported input format: {path.name}")
    log.info(f"Loaded data from {path}...")
    return data


def save_toml(data: TOMLDocument, path: Optional[Path] = None):
    """Save tomlkit TOMLDocument object into toml file.

    Supports .toml extension. It retains the indentation and comments in the toml file.
    :param data: tomlkit TOMLDocument object containing configurations
    :param path: path to file
    """
    if path is not None:
        log.debug(f"Saving tomlkit TOMLDocument object to {path}...")
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.name.endswith(".toml"):
            with open(path, mode="w", encoding="utf-8") as f:
                tomlkit.dump(data, f)
        else:
            raise ValueError(f"Unsupported format: {path.name}")
        log.info(f"Saved tomlkit TOMLDocument object to {path}")


def extract_filename_components(filename: str) -> Dict[str, str] | None:
    """Extract the file components from file key.

    :param filename: File name.
    :return: Dictionary of extracted components from file.
    """
    path = Path(filename)
    components = path.stem.split("-")
    if len(components) != 4:
        return None
    deployment, business_unit, language, remaining_part = components
    article_type, mode, date = remaining_part.split("_")
    return {
        "business_unit": business_unit,
        "language": language,
        "deployment": deployment,
        "article_type": article_type,
        "mode": mode,
        "date": date,
    }

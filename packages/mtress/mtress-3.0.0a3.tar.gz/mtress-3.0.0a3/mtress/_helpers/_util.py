"""Utility functions."""

import dataclasses
import inspect
from pathlib import Path
from typing import Any

import pandas as pd


def update_in_dict(
    dictionary: dict,
    keys: list[str] | str,
    value: Any,
    sep: str = ".",
    ignore_missing: bool = True,
) -> None:
    """
    Update value in nested dictionary.

    `update_in_dict(d, ['foo', 'bar', 'baz'], 3.1415)` or
    `update_in_dict(d, 'foo.bar.baz', 3.1415)` are equivalent to
    `d['foo']['bar']['baz'] = 3.1415`.

    :param dictionary: Dictionary which should be updated
    :param keys: List of keys or dot separated string locating the value in question
    :param value: New value
    :param sep: Level separator, defaults to .
    :param ignore_missing: Ignore missing keys
    """
    if isinstance(keys, str):
        keys = keys.split(sep)

    *keys, key = keys
    for level in keys:
        if ignore_missing and level not in dictionary:
            dictionary[level] = {}
        dictionary = dictionary[level]

    dictionary[key] = value


def get_from_dict(
    dictionary: dict,
    keys: list[str] | str,
    sep: str = ".",
    default: Any = None,
) -> Any:
    """
    Get value from nested dictionary.

    :param dictionary: Dictionary to get a avalue from
    :param keys: List of keys or dot separated string locating the value
    :param sep: Level seperator, defaults to .
    :param default: Default value, if key is not present

    """
    if isinstance(keys, str):
        keys = keys.split(sep)

    for key in keys:
        if key not in dictionary and default is not None:
            return default

        dictionary = dictionary[key]

    return dictionary


def _read_csv_data(file: Path, column: str) -> pd.Series:
    """
    Read a column from a CSV file.

    This functions reads a CSV file and returns the specified column. The first
    column of the file is expected to be an UTC time index.

    :param file: File to read from
    :param column: Column name
    """
    _df = pd.read_csv(file, index_col=0, usecols=[column], parse_dates=True)

    return _df[column]


_data_parsers = {"csv": _read_csv_data}


def read_input_data(data_specifier: str) -> pd.Series:
    """
    Read a time series from a file.

    Supported file formats are:
    - CSV

    :param data_specifier: Data specifier
    """
    filepath, specifier = data_specifier.split(":", maxsplit=1)

    file = Path(filepath)
    assert file.exists(), f"File {filepath} does not exist"

    _suffix = file.suffix.lower()
    if _suffix not in _data_parsers:
        raise KeyError(f"Don't know how to read {filepath}")

    _parser = _data_parsers[_suffix]
    return _parser(file, specifier)


def enable_templating(template_class):
    """Decorate a function to accept a dataclass as a template."""

    def _decorator(func):
        param_names = [field.name for field in dataclasses.fields(template_class)]
        func_signature = inspect.signature(func)
        func_params = func_signature.parameters

        def _wrapper(*args, template=None, **kwargs):
            if template is not None:
                if not isinstance(template, template_class):
                    raise TypeError(f"template should be of type {template_class}")

                for param in param_names:
                    if param not in kwargs and param in func_params:
                        # Take the value from the template if it is not provided as keyword
                        # argument
                        kwargs[param] = getattr(template, param)

            return func(*args, **kwargs)

        return _wrapper

    return _decorator

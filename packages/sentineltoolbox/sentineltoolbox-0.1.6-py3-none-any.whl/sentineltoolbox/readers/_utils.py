import json
import logging
from pathlib import Path
from typing import Any, BinaryIO, Literal

import tomli

from sentineltoolbox.typedefs import is_eopf_adf

logger = logging.getLogger("sentineltoolbox")


L_SUPPORTED_FORMATS = Literal[".json", ".toml", ".txt", None]

stb_open_parameters = ("secret_alias", "logger", "credentials", "configuration")


def load_toml_fp(fp: BinaryIO) -> dict[str, Any]:
    with fp:
        return tomli.load(fp)


def load_toml(path: Path) -> dict[str, Any]:
    with open(str(path), mode="rb") as fp:
        return load_toml_fp(fp)


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as json_fp:
        return json.load(json_fp)


def is_eopf_adf_loaded(path_or_pattern: Any) -> bool:
    """

    :param path_or_pattern:
    :return:
    """
    return is_eopf_adf(path_or_pattern) and path_or_pattern.data_ptr is not None


def _cleaned_kwargs(kwargs: Any) -> dict[str, Any]:
    cleaned = {}
    for kwarg in kwargs:
        if kwarg not in stb_open_parameters:
            cleaned[kwarg] = kwargs[kwarg]
    return cleaned


def fix_kwargs_for_lazy_loading(kwargs: Any) -> None:
    if "chunks" not in kwargs:
        kwargs["chunks"] = {}
    else:
        if kwargs["chunks"] is None:
            raise ValueError(
                "open_datatree(chunks=None) is not allowed. Use load_datatree instead to avoid lazy loading data",
            )

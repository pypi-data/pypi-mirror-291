import json
import logging
from pathlib import Path
from typing import Any

import fsspec

from sentineltoolbox._utils import split_protocol
from sentineltoolbox.exceptions import LoadingDataError
from sentineltoolbox.filesystem_utils import get_url_and_credentials
from sentineltoolbox.readers._utils import is_eopf_adf_loaded
from sentineltoolbox.typedefs import Credentials, PathMatchingCriteria, PathOrPattern


def is_json(path: str) -> bool:
    suffixes: str = "".join(Path(path).suffixes)
    # TODO: path.is_file() and
    return suffixes in {".json", ".json.zip"}


def open_json(
    path_or_pattern: PathOrPattern,
    *,
    credentials: Credentials | None = None,
    match_criteria: PathMatchingCriteria = "last_creation_date",
    **kwargs: Any,
) -> dict[Any, Any]:
    if is_eopf_adf_loaded(path_or_pattern) and isinstance(path_or_pattern.data_ptr, dict):
        return path_or_pattern.data_ptr
    url, credentials = get_url_and_credentials(
        path_or_pattern,
        credentials=credentials,
        match_criteria=match_criteria,
        **kwargs,
    )
    protocols, relurl = split_protocol(url)

    if credentials:
        fs = fsspec.filesystem(**credentials.to_kwargs(target=fsspec.filesystem))
        if "zip" in protocols:
            zipfs = fsspec.filesystem("zip", fo=fs.open(f"s3://{relurl}"))
            url = zipfs.ls("/")[0]["filename"]
            open_func = zipfs.open
        else:
            open_func = fs.open
    elif url.endswith(".zip"):
        zipfs = fsspec.filesystem("zip", fo=str(relurl))
        url = zipfs.ls("/")[0]["filename"]
        open_func = zipfs.open
    else:
        open_func = open
        url = str(relurl)

    logger = kwargs.get("logger", logging.getLogger("sentineltoolbox"))
    logger.info(f"open {url}")
    try:
        with open_func(url, "r", encoding="utf-8") as json_fp:
            return json.load(json_fp)
    except json.JSONDecodeError:
        raise LoadingDataError(url)


def load_json(
    path_or_pattern: PathOrPattern,
    *,
    credentials: Credentials | None = None,
    match_criteria: PathMatchingCriteria = "last_creation_date",
    **kwargs: Any,
) -> dict[Any, Any]:
    return open_json(path_or_pattern, credentials=credentials, match_criteria=match_criteria, **kwargs)

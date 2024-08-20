import datetime
import logging
from copy import copy
from pathlib import Path, PurePosixPath
from typing import Any

import fsspec
import s3fs

from sentineltoolbox._utils import _credential_required, fix_url, split_protocol
from sentineltoolbox.configuration import get_config
from sentineltoolbox.exceptions import MultipleResultsError
from sentineltoolbox.models.credentials import S3BucketCredentials
from sentineltoolbox.models.filename_generator import detect_filename_pattern
from sentineltoolbox.models.upath import PathFsspec
from sentineltoolbox.typedefs import (
    Credentials,
    DataPath,
    PathOrPattern,
    fix_datetime,
    is_any_path,
    is_eopf_adf,
)

logger = logging.getLogger("sentineltoolbox")


def get_directory_mtime(
    fs: fsspec.spec.AbstractFileSystem,
    path: str,
    preferred: str = ".zmetadata",
) -> datetime.datetime:
    file_path = None
    for child_path in fs.ls(path):
        child_name = PurePosixPath(child_path).name
        if fs.isfile(child_path):
            file_path = child_path
            if child_name == preferred:
                break
    if file_path is None:
        return datetime.datetime.now()
    else:
        return fs.modified(file_path)


def _get_fsspec_filesystem_from_url_and_credentials(url: str, credentials: Credentials | None, **kwargs: Any) -> Any:
    protocols, relurl = split_protocol(url)
    if "filesystem" in kwargs:
        return kwargs["filesystem"], relurl
    else:
        if credentials:
            fsspec_options = credentials.to_kwargs(target=fsspec.filesystem)
        else:
            fsspec_options = {"protocol": "::".join(protocols)}
            fsspec_options["protocol"] = fsspec_options["protocol"].replace("zip::file", "file")
            fsspec_options["protocol"] = fsspec_options["protocol"].replace("file::zip", "file")
        return fsspec.filesystem(**fsspec_options), relurl


def get_fsspec_filesystem(
    path_or_pattern: PathOrPattern,
    **kwargs: Any,
) -> tuple[Any, PurePosixPath]:
    """
    Function to instantiate fsspec.filesystem from url.
    Return path relative to filesystem. Can be absolute or not depending on fs.
    This function clean url and extract credentials (if necessary) for you.

    >>> fs, root = get_fsspec_filesystem("tests")
    >>> fs, root = get_fsspec_filesystem("s3://s3-input/Products/", secret_alias="s3-input") # doctest: +SKIP
    >>> fs.ls(root) # doctest: +SKIP

    See `fsspec documentation <https://filesystem-spec.readthedocs.io/en/latest/usage.html>`_

    :param path_or_pattern: path to use to build filesystem
    :param kwargs: see generic input parameters in :obj:`sentineltoolbox.typedefs` module
    :return: fsspec.AbstractFileSystem, path relative to filesystem
    """
    url, credentials = get_url_and_credentials(path_or_pattern, **kwargs)
    kwargs["credentials"] = credentials
    return _get_fsspec_filesystem_from_url_and_credentials(url=url, **kwargs)


def get_universal_path(
    path_or_pattern: PathOrPattern,
    **kwargs: Any,
) -> DataPath:
    """
    Return a universal Path: a path following pathlib.Path api but supporting all kind of path (local, s3 bucket, ...)
    thanks to fsspec. fsspec/universal_pathlib is the candidate for this but is not enough mature for the moment
    (for example, protocol chaining is not supported, see https://github.com/fsspec/universal_pathlib/issues/28)
    So we define ...
      - protocol DataPath: a subset of pathlib.Path
      - PathFsspec: an implementation of DataPath based on fsspec, used until UPath doesn't work with chaining
      - upath.UPath: will be used as soon as possible

    :param path_or_pattern:
    :param kwargs:
    :return:
    """
    fs, relurl = get_fsspec_filesystem(path_or_pattern, **kwargs)
    return PathFsspec(str(relurl), fs=fs)


def resolve_pattern(pattern: str | Path, credentials: Credentials | None = None, **kwargs: Any) -> str:
    match_criteria = kwargs.get("match_criteria", "last_creation_date")
    protocols, relurl = split_protocol(str(pattern))
    if "filesystem" in kwargs:
        fs: fsspec.spec.AbstractFileSystem = kwargs["filesystem"]
    else:
        if "zip" in protocols:
            # first check that path exists and is not a pattern
            resolve_protocols = copy(protocols)
            resolve_protocols.remove("zip")
            # resolve_protocols.add("file")
            fs = fsspec.filesystem("::".join(resolve_protocols))
        else:
            if credentials:
                fs = fsspec.filesystem(**credentials.to_kwargs(target=fsspec.filesystem))
            else:
                fs = fsspec.filesystem("::".join(protocols))
    paths = fs.expand_path(str(relurl))

    if not paths:
        raise ValueError(f"Invalid pattern {pattern!r}")
    elif len(paths) == 1:
        return fix_url("::".join(protocols) + "://" + str(paths[0]))
    elif len(paths) > 1:
        dates = {}
        for path in paths:
            ftype = detect_filename_pattern(path)
            if ftype.startswith("adf") and match_criteria == "last_creation_date":
                creation_date = fix_datetime(PurePosixPath(path).name.split(".")[0].split("_")[-1])
            else:
                try:
                    creation_date = fs.modified(path)
                except IsADirectoryError:
                    creation_date = get_directory_mtime(fs, path)
            dates[path] = creation_date

        last, last_date = None, datetime.datetime(1, 1, 1, 1, tzinfo=datetime.timezone.utc)
        for path, creation_date in dates.items():
            if creation_date > last_date:
                last = path
                last_date = creation_date
            elif creation_date == last_date:
                raise MultipleResultsError(
                    f"cannot select file from pattern {pattern}.\n"  # nosec B608
                    f"files {last} and {path} have same creation date",  # nosec B608
                )
        if last:
            url = fix_url("::".join(protocols) + "://" + str(last))
            logger.info(f"Select {url!r} for pattern {pattern!r}")
            return url
        else:
            raise ValueError(f"cannot select file from pattern {pattern}")  # nosec B608
    else:
        raise ValueError(f"Cannot expand pattern {pattern!r}: result: {paths}")  # nosec B608


def _get_url_and_credentials_from_eopf_inputs(
    path_or_pattern: PathOrPattern,
    **kwargs: Any,
) -> tuple[str, Credentials | None]:
    credentials = kwargs.get("credentials")
    if is_eopf_adf(path_or_pattern):
        any_path = path_or_pattern.path
        if not is_any_path(any_path):
            return any_path, credentials
        if not path_or_pattern.store_params:
            if isinstance(any_path._fs, s3fs.S3FileSystem):
                storage_options = any_path._fs.storage_options
            else:
                storage_options = {}
        else:
            storage_options = path_or_pattern.store_params["storage_options"]
    else:
        any_path = path_or_pattern
        if "ADF" in str(any_path.original_url):
            logger.warning(
                "For ADF, prefer passing whole AuxiliaryDataFile/ADF object instead of AuxiliaryDataFile.path",
            )
        if isinstance(any_path._fs, s3fs.S3FileSystem):
            storage_options = any_path._fs.storage_options
        else:
            storage_options = {}
    try:
        url = str(any_path.original_url)
    except AttributeError:
        url = str(any_path)
    try:
        url = resolve_pattern(url, **kwargs)
    except NotImplementedError:
        pass
    if _credential_required(url, credentials):
        credentials = S3BucketCredentials.from_kwargs(**storage_options)
    return url, credentials


def get_url_and_credentials(
    path_or_pattern: PathOrPattern,
    **kwargs: Any,
) -> tuple[str, Credentials | None]:
    """
    Function that cleans url and extract credentials (if necessary) for you.

    :param path_or_pattern:
    :param credentials:
    :param kwargs:
    :return:
    """
    credentials = kwargs.get("credentials")
    if isinstance(path_or_pattern, (str, Path)):
        url = fix_url(str(path_or_pattern))
        conf = get_config(**kwargs)
        secret_alias = conf.get_secret_alias(url)
        if secret_alias:
            kwargs["secret_alias"] = secret_alias
        if _credential_required(url, credentials):
            credentials = S3BucketCredentials.from_env(**kwargs)
        try:
            kwargs["credentials"] = credentials
            url = resolve_pattern(path_or_pattern, **kwargs)
        except NotImplementedError:
            url = str(path_or_pattern)

    elif is_eopf_adf(path_or_pattern) or is_any_path(path_or_pattern):
        url, credentials = _get_url_and_credentials_from_eopf_inputs(path_or_pattern, **kwargs)
    elif isinstance(path_or_pattern, PathFsspec):
        credentials = S3BucketCredentials.from_kwargs(**path_or_pattern.options)
        url = path_or_pattern.path
    else:
        raise NotImplementedError(f"path {path_or_pattern} of type {type(path_or_pattern)} is not supported yet")

    kwargs["credentials"] = credentials
    return url, credentials

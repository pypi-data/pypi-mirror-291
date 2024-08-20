from pathlib import Path, PurePosixPath
from typing import Any

from sentineltoolbox.typedefs import Credentials


def split_protocol(url: str) -> tuple[set[str], PurePosixPath]:
    url_str = str(url)
    if "://" in url_str:
        parts = url_str.split("://")
        protocol = parts[0]
        path = parts[1]
        if not protocol:
            protocol = "file"
    else:
        protocol = "file"
        path = url_str
    return set(protocol.split("::")), PurePosixPath(path)


def fix_url(url: str) -> str:
    """
    Fix url to get always same protocols and protocol order.

    >>> fix_url("test.txt")
    'file://test.txt'
    >>> fix_url("/d/test.txt")
    'file:///d/test.txt'
    >>> fix_url("D:\\test.txt")
    'file://D:\\test.txt'
    >>> fix_url("s3://test")
    's3://test'
    >>> fix_url("s3://")
    's3://'
    >>> fix_url("://test")
    'file://test'
    >>> fix_url("://")
    'file://'
    >>> fix_url("zip::s3://")
    'zip::s3://'
    >>> fix_url("s3::zip://")
    'zip::s3://'
    >>> fix_url("s3://test.zip")
    'zip::s3://test.zip'


    :param url:
    :return:
    """
    protocols, relurl = split_protocol(url)
    # add protocols based on extensions
    if Path(str(url)).suffix == ".zip":
        protocols.add("zip")

    # build valid_protocol list
    # remove conflicts like zip::file
    # force order like zip::s3
    valid_protocols = []
    for p in ["zip", "s3"]:
        if p in protocols:
            valid_protocols.append(p)
            protocols.remove(p)
    valid_protocols += list(protocols)
    # if len(valid_protocols) > 1 and "file" in valid_protocols:
    #    valid_protocols.remove("file")

    protocol = "::".join(valid_protocols)
    if str(relurl) == ".":
        return f"{protocol}://"
    else:
        return f"{protocol}://{relurl}"


def _is_s3_url(url: str) -> bool:
    protocols, path = split_protocol(url)
    return "s3" in protocols


def _credential_required(url: str, credentials: Credentials | None) -> bool:
    protocols, path = split_protocol(url)
    return "s3" in protocols and credentials is None


def string_to_slice(s: str) -> slice:
    """
    Convert a string in the format "start:stop:step" to a Python slice object.

    :param s: String representing the slice.
    :return: Corresponding Python slice object.
    """
    # Split the string by colon to get start, stop, and step parts
    parts: list[str | Any] = s.split(":")

    # If the string contains fewer than three parts, append None for missing values
    while len(parts) < 3:
        parts.append(None)

    # Convert the parts to integers or None
    start = int(parts[0]) if parts[0] else None
    stop = int(parts[1]) if parts[1] else None
    step = int(parts[2]) if parts[2] else None

    # Create and return the slice object
    return slice(start, stop, step)


def patch(instance: Any, manager_class: Any, **kwargs: Any) -> None:
    manager = manager_class(instance, **kwargs)

    for attr_name in dir(manager):
        if attr_name.startswith("_"):
            continue
        attr = getattr(manager, attr_name)
        if callable(attr):
            try:  # if method existed before, save it to _method
                setattr(instance, "_" + attr_name, getattr(instance, attr_name))
            except AttributeError:
                pass
            setattr(instance, attr_name, attr)

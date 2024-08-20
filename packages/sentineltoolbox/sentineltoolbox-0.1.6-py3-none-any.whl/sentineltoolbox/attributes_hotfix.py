import datetime
import logging
from typing import Any

from sentineltoolbox.typedefs import MetadataType_L, fix_datetime

"""
Some useful links:
https://eoframework.esa.int/display/CDSE/Copernicus+Data+Space+Ecosystem+%28CDSE%29+STAC+catalogue
"""

logger = logging.getLogger("sentineltoolbox")

valid_aliases: dict[str, str] = {"eo:bands": "bands", "eopf:type": "product:type", "eopf:timeline": "product:timeline"}

short_names_stac_properties_root: set[str] = {"bands", "platform", "product:type", "processing:version"}
short_names_stac_root: set[str] = set()
short_names_metadata_root: set[str] = {"title"}

# ex: 'vara': 'gr/subgr/vara'
short_names_stac_properties: dict[str, str] = {}
short_names_stac: dict[str, str] = {}
short_names_metadata: dict[str, str] = {}

legacy_aliases = {v: k for k, v in valid_aliases.items()}
attribute_short_names: dict[str, tuple[MetadataType_L, str]] = {}

for key, path in short_names_stac_properties.items():
    attribute_short_names[key] = ("stac_properties", path)
for key, path in short_names_stac.items():
    attribute_short_names[key] = ("stac_discovery", path)
for key, path in short_names_metadata.items():
    attribute_short_names[key] = ("metadata", path)

for key in short_names_stac_properties_root:
    attribute_short_names[key] = ("stac_properties", key)
for key in short_names_stac_root:
    attribute_short_names[key] = ("stac_discovery", key)
for key in short_names_metadata_root:
    attribute_short_names[key] = ("metadata", key)


for legacy, valid in valid_aliases.items():
    if valid in attribute_short_names:
        attribute_short_names[legacy] = attribute_short_names[valid]


def to_lower(value: str, **kwargs: Any) -> str:
    path = kwargs.get("path", "value")
    new_value = value.lower()
    if value != new_value:
        logger.warning(f"{path}: value {value!r} has been fixed to {new_value!r}")
    return new_value


def to_datetime(value: str, **kwargs: Any) -> datetime.datetime:
    return fix_datetime(value)


convert_functions = {
    "stac_properties": {
        "platform": to_lower,
        "created": to_datetime,
        "end_datetime": to_datetime,
        "start_datetime": to_datetime,
    },
}

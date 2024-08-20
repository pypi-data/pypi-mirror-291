from pathlib import Path

from sentineltoolbox.configuration import Configuration

UT_DATA = Path("tests/ut/data/")
IT_DATA = "s3://buc-acaw-dpr/testdata/sentineltoolbox/ut/data/"


def home_path_empty() -> Path:
    """
    mocked return function to replace Path.home
    always return valid but empty directory
    """
    return Path("tests/ut/data/empty")


def home_path_sample() -> Path:
    """
    mocked return function to replace Path.home
    always return valid but empty directory
    """
    return Path("tests/ut/data/home")


def configuration_sample() -> Configuration:
    conf = Configuration(path=home_path_sample() / ".eopf/sentineltoolbox.toml")
    conf.data["resources"]["sentineltoolbox.resources"] = [home_path_sample() / "resources"]
    return conf

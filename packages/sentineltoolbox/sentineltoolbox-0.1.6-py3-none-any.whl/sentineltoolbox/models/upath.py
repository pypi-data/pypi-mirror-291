import os
from pathlib import PurePosixPath
from typing import Any, Generator

from sentineltoolbox.typedefs import DataPath


class PathFsspec(DataPath):
    """
    Class to manage Amazon S3 Bucket.
    This path must be absolute and must start with s3://
    """

    def __init__(
        self,
        path: str,
        fs: Any,
        **kwargs: Any,
    ) -> None:
        """
        Parameters
        ----------
        path
            s3 absolute path
        fs
            fsspec.filesystem

        Raises
        ------
        ValueError
            if path is not an absolute s3 path
        """
        self.fs = fs
        self.options = kwargs.get("options", {})
        super().__init__(str(path))

    # docstr-coverage: inherited
    def is_file(self) -> bool:
        return self.fs.isfile(self.path)

    # docstr-coverage: inherited
    def is_dir(self) -> bool:
        return self.fs.isdir(self.path)

    # docstr-coverage: inherited
    @property
    def name(self) -> str:
        return PurePosixPath(self.path).name

    # docstr-coverage: inherited
    @property
    def parent(self) -> str:
        return "/".join(str(self.path).split("/")[:-1])

    def stat(self, *, follow_symlinks: bool = True) -> os.stat_result:
        """
        Returns information about this path (similarly to boto3's ObjectSummary).
        For compatibility with pathlib, the returned object some similar attributes like os.stat_result.
        The result is looked up at each call to this method
        """
        # os.stat_result(st_mode=1, st_ino=2, st_dev=3, st_nlink=4, st_uid=5, st_gid=6, st_size=7, st_atime=8,
        # st_mtime=9, st_ctime=10)
        st_mode = -1
        st_ino = -1
        st_dev = -1
        st_nlink = -1
        st_uid = -1
        st_gid = -1
        st_size: float = self.fs.size(self.path)
        st_atime = -1
        try:
            st_mtime: float = self.fs.modified(self.path).timestamp()
        except IsADirectoryError:
            st_mtime = 0
        st_ctime = -1
        return os.stat_result(
            (
                st_mode,
                st_ino,
                st_dev,
                st_nlink,
                st_uid,
                st_gid,
                st_size,
                st_atime,
                st_mtime,
                st_ctime,
            ),
        )

    def open(
        self,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        errors: str | None = None,
        newline: Any = None,
    ) -> Any:
        # path, mode='rb', block_size=None, cache_options=None, compression=None, **kwargs
        return self.fs.open(
            self.path,
            mode=mode,
            compression="infer",
            encoding=encoding,
            errors=errors,
        )

    def exists(self) -> bool:
        return self.fs.exists(self.path)

    def glob(self, pattern: str) -> Generator[DataPath, None, None]:
        for relpath in self.fs.glob(f"{self.path}/{pattern}"):
            yield self.__class__(relpath, fs=self.fs)

    def rglob(self, pattern: str) -> Generator[DataPath, None, None]:
        for relpath in self.fs.glob(f"{self.path}/**/{pattern}"):
            yield self.__class__(relpath, fs=self.fs)

    @property
    def url(self) -> str:
        return self.fs.protocol[0] + "://" + self.path

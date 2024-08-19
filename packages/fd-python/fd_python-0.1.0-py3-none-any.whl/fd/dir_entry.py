from enum import Enum
import ignore
import os
import pathlib

from .config import Config
from .filesystem import strip_current_dir


class DirEntry(Enum):
    NORMAL = 1
    BROKEN_SYMLINK = 2

    inner: ignore.DirEntry | pathlib.Path

    @classmethod
    def normal(cls, e: ignore.DirEntry):
        instance = cls(DirEntry.NORMAL)
        instance.inner = e

        return instance

    @classmethod
    def broken_symlink(cls, path: pathlib.Path):
        instance = cls(DirEntry.BROKEN_SYMLINK)
        instance.inner = path

        return instance

    def path(self) -> pathlib.Path:
        return self.inner.path() if self == DirEntry.NORMAL else self.inner

    def stripped_path(self, config: Config) -> pathlib.Path:
        return strip_current_dir(self.path()) if config.strip_cwd_prefix else self.path()

    def stat(self) -> os.stat_result:
        return self.inner.path().stat()

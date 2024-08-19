import os
import pathlib
import sys

from .config import Config
from .dir_entry import DirEntry


def replace_path_separator(path, new_path_separator):
    raise NotImplementedError("`replace_path_separator` not implemented!")


def print_entry(entry: DirEntry, config: Config):
    print_entry_uncolorized(entry, config)

    if config.null_separator:
        sys.stdout.write("\0")
    else:
        sys.stdout.write(os.linesep)


def print_entry_uncolorized(entry: DirEntry, config: Config):
    path_string: pathlib.Path = entry.stripped_path(config)

    if config.path_separator:
        path_string = replace_path_separator(path_string, config.path_separator)

    sys.stdout.write(str(path_string))

    print_trailing_slash(entry, config)


def print_trailing_slash(entry: DirEntry, config: Config):
    if entry.path().is_dir():
        sys.stdout.write(config.actual_path_separator)

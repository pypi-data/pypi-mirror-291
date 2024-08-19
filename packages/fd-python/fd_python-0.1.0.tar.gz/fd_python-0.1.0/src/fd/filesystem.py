import pathlib


def strip_current_dir(path: pathlib.Path) -> pathlib.Path:
    return path.relative_to(".")

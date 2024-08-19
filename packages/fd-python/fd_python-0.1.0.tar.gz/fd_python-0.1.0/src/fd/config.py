from dataclasses import dataclass
import pathlib

from .filter.size import SizeFilter


@dataclass
class Config:
    """Configuration options for *fd*."""
    
    case_sensitive: bool
    """Whether the search is case-sensitive or case-insensitive."""

    search_full_path: bool
    """Whether to search within the full file path or just the base name (filename or directory
    name)."""

    ignore_hidden: bool
    """Whether to ignore hidden files and directories (or not)."""

    read_fdignore: bool
    """Whether to respect `.fdignore` files or not."""

    read_parent_ignore: bool
    """Whether to respect ignore files in parent directories or not."""

    read_vcsignore: bool
    """Whether to respect VCS ignore files (`.gitignore`, ..) or not."""

    require_git_to_read_vcsignore: bool
    """Whether to require a `.git` directory to respect gitignore files."""

    follow_links: bool
    """Whether to follow symlinks or not."""

    one_file_system: bool
    """Whether to follow symlinks or not."""

    null_separator: bool
    """Whether elements of output should be separated by a null character"""

    max_depth: int | None
    """The maximum search depth, or `None` if no maximum search depth should be set.

    A depth of `1` includes all files under the current directory, a depth of `2` also includes
    all files under subdirectories of the current directory, etc."""

    min_depth: int | None
    """The minimum depth for reported entries, or `None`."""

    quiet: bool
    """If true, the program doesn't print anything and will instead return an exit code of 0
    if there's at least one match. Otherwise, the exit code will be 1."""

    exclude_patterns: list[str]
    """A list of glob patterns that should be excluded from the search."""

    ignore_files: list[pathlib.Path]
    """A list of custom ignore files."""

    size_constraints: list[SizeFilter]
    """The given constraints on the size of returned files"""

    show_filesystem_errors: bool
    """Whether or not to display filesystem errors"""

    path_separator: str | None
    """The separator used to print file paths."""

    actual_path_separator: str
    """The actual separator, either the system default separator or `path_separator`"""

    max_results: int | None
    """The maximum number of search results"""

    strip_cwd_prefix: bool
    """Whether or not to strip the './' prefix for search results"""

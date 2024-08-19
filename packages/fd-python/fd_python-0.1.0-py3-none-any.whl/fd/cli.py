import argparse
from dataclasses import dataclass
import pathlib
from typing import Callable

from .__about__ import __version__
from .filter.size import SizeFilter


@dataclass
class Opts:
    @classmethod
    def parse(cls):
        return cls()

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="fd",
            description="A program to find entries in your filesystem",
            formatter_class=argparse.RawTextHelpFormatter
        )

        parser.add_argument(
            "--version", "-V",
            action='version',
            version='%(prog)s ' + __version__
        )
        parser.add_argument(
            "-H", "--hidden",
            action="store_true",
            help=
"""Include hidden directories and files in the search results (default:
hidden files and directories are skipped). Files and directories are
considered to be hidden if their name starts with a `.` sign (dot).
Any files or directories that are ignored due to the rules described by
--no-ignore are still ignored unless otherwise specified.
The flag can be overridden with --no-hidden."""
        )
        parser.add_argument(
            "--no-hidden",
            action="store_true",
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            "--no-ignore", "-I",
            action="store_true",
            help=
"""Show search results from files and directories that would otherwise be
ignored by '.gitignore', '.ignore', or '.fdignore'.
The flag can be overridden with --ignore."""
        )
        parser.add_argument(
            "--ignore",
            action="store_true",
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            "--no-ignore-vcs",
            action="store_true",
            help=
"""Show search results from files and directories that
would otherwise be ignored by '.gitignore' files.
The flag can be overridden with --ignore-vcs."""
        )
        parser.add_argument(
            "--ignore-vcs",
            action="store_true",
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            "--no-require-git",
            action="store_true",
            help=
"""Do not require a git repository to respect gitignores.
By default, fd will only respect .gitignore rules,
and local exclude rules if fd detects that you are searching inside a
git repository. This flag allows you to relax this restriction such that
fd will respect all git related ignore rules regardless of whether you're
searching in a git repository or not.


This flag can be disabled with --require-git."""
        )
        parser.add_argument(
            "--require-git",
            action="store_true",
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            "--no-ignore-parent",
            action="store_true",
            help=
"""Show search results from files and directories that would otherwise be
ignored by '.gitignore', '.ignore', or '.fdignore' files in parent directories."""
        )
        parser.add_argument(
            "--unrestricted", "-u",
            action="count",
            default=0,
            dest="rg_alias_hidden_ignore",
            help=
"""Perform an unrestricted search, including ignored and hidden files. This is
an alias for '--no-ignore --hidden'."""
        )
        parser.add_argument(
            "-s", "--case-sensitive",
            action="store_true",
            help=
"""Perform a case-sensitive search. By default, fd uses case-insensitive
searches, unless the pattern contains an uppercase character (smart
case)."""
        )
        parser.add_argument(
            "-i", "--ignore-case",
            action="store_true",
            help=
"""Perform a case-insensitive search. By default, fd uses case-insensitive
searches, unless the pattern contains an uppercase character (smart
case)."""
        )
        parser.add_argument(
            "-g", "--glob",
            action="store_true",
            help=
"""Perform a glob-based search instead of a regular expression search."""
        )
        parser.add_argument(
            "--regex",
            action="store_true",
            help=
"""Perform a regular-expression based search (default). This can be used to
override --glob."""
        )
        parser.add_argument(
            "-F", "--fixed-strings", "--literal",
            action="store_true",
            help=
"""Treat the pattern as a literal string instead of a regular expression. Note
that this also performs substring comparison. If you want to match on an
exact filename, consider using '--glob'."""
        )
        parser.add_argument(
            "--and",
            action="append",
            default=[],
            dest="exprs",
            metavar="PATTERN",
            help=
"""Add additional required search patterns, all of which must be matched. Multiple
additional patterns can be specified. The patterns are regular
expressions, unless '--glob' or '--fixed-strings' is used."""
        )
        parser.add_argument(
            "--absolute-path", "-a",
            action="store_true",
            help=
"""Shows the full path starting from the root as opposed to relative paths.
The flag can be overridden with --relative-path."""
        )
        parser.add_argument(
            "--relative-path",
            action="store_true",
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            "--follow", "-L", "--dereference",
            action="store_true",
            help=
"""By default, fd does not descend into symlinked directories. Using this
flag, symbolic links are also traversed.
Flag can be overridden with --no-follow."""
        )
        parser.add_argument(
            "no-follow",
            action="store_true",
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            "-p", "--full-path",
            action="store_true",
            help=
"""By default, the search pattern is only matched against the filename
(or directory name). Using this flag, the pattern is matched against
the full (absolute) path. Example:
  fd --glob -p '**/.git/config'"""
        )
        parser.add_argument(
            "--print0", "-0",
            action="store_true",
            dest="null_separator",
            help=
"""Separate search results by the null character (instead of newlines).
Useful for piping results to 'xargs'."""
        )
        parser.add_argument(
            "--max-depth", "-d", "--maxdepth",
            metavar="DEPTH",
            dest="_max_depth",
            type=int,
            help=
"""Limit the directory traversal to a given depth. By default, there is no
limit on the search depth."""
        )
        parser.add_argument(
            "--min-depth",
            metavar="DEPTH",
            dest="_min_depth",
            type=int,
            help=
"""Only show search results starting at the given depth.
See also: '--max-depth' and '--exact-depth'"""
        )
        parser.add_argument(
            "--exact-depth",
            metavar="DEPTH",
            type=int,
            help=
"""Only show search results at the exact given depth. This is an alias for
'--min-depth <depth> --max-depth <depth>'."""
        )
        parser.add_argument(
            "--exclude", "-E",
            action="append",
            default=[],
            metavar="PATTERN",
            help=
"""Exclude files/directories that match the given glob pattern. This
overrides any other ignore logic. Multiple exclude patterns can be
specified.

Examples:
{n}  --exclude '*.pyc'
{n}  --exclude node_modules"""
        )
        parser.add_argument(
            "--size", "-S",
            action="append",
            type=SizeFilter.from_string,
            help=
"""Limit results based on the size of files using the format <+-><NUM><UNIT>.
   '+': file size must be greater than or equal to this
   '-': file size must be less than or equal to this

If neither '+' nor '-' is specified, file size must be exactly equal to this.
   'NUM':  The numeric size (e.g. 500)
   'UNIT': The units for NUM. They are not case-sensitive.
Allowed unit values:
    'b':  bytes
    'k':  kilobytes (base ten, 10^3 = 1000 bytes)
    'm':  megabytes
    'g':  gigabytes
    't':  terabytes
    'ki': kibibytes (base two, 2^10 = 1024 bytes)
    'mi': mebibytes
    'gi': gibibytes
    'ti': tebibytes"""
        )
        parser.add_argument(
            "--ignore-file",
            action="append",
            default=[],
            metavar="PATH",
            type=pathlib.Path,
            help=
"""Add a custom ignore-file in '.gitignore' format. These files have a low precedence."""
        )
        parser.add_argument(
            "--max-results",
            metavar="COUNT",
            dest="_max_results",
            type=int,
            help=
"""Limit the number of search results to 'count' and quit immediately."""
        )
        parser.add_argument(
            "--max-one-result", "-1",
            action="store_true",
            dest="_max_one_result",
            help=
"""Limit the search to a single result and quit immediately.
This is an alias for '--max-results=1'."""
        )
        parser.add_argument(
            "--quiet", "-q", "--has-results",
            action="store_true",
            help=
"""When the flag is present, the program does not print anything and will
return with an exit code of 0 if there is at least one match. Otherwise, the
exit code will be 1.
'--has-results' can be used as an alias."""
        )
        parser.add_argument(
            "--show-errors",
            action="store_true",
            help=
"""Enable the display of filesystem errors for situations such as
insufficient permissions or dead symlinks."""
        )
        parser.add_argument(
            "--base-directory",
            type=pathlib.Path,
            help=
"""Change the current working directory of fd to the provided path. This
means that search results will be shown with respect to the given base
path. Note that relative paths which are passed to fd via the positional
<path> argument or the '--search-path' option will also be resolved
relative to this directory."""
        )
        parser.add_argument(
            "pattern",
            default='',
            nargs="?",
            help=
"""The search pattern which is either a regular expression (default) or a glob
pattern (if --glob is used). If no pattern has been specified, every entry
is considered a match. If your pattern starts with a dash (-), make sure to
pass '--' first, or it will be considered as a flag (fd -- '-foo')."""
        )
        parser.add_argument(
            "--path-separator",
            metavar="SEPARATOR",
            help=
"""Set the path separator to use when printing file paths. The default is
the OS-specific separator ('/' on Unix, '\' on Windows)."""
        )
        parser.add_argument(
            "path",
            nargs="*",
            type=pathlib.Path,
            help=
"""The directory where the filesystem search is rooted (optional). If
omitted, search the current working directory."""
        )
        parser.add_argument(
            "--search-path",
            action="append",
            default=[],
            type=pathlib.Path,
            help=
"""Provide paths to search as an alternative to the positional <path>
argument. Changes the usage to `fd [OPTIONS] --search-path <path>
--search-path <path2> [<pattern>]`"""
        )
        parser.add_argument(
            "--strip-cwd-prefix",
            action="store_true",
            dest="_strip_cwd_prefix",
            help=
"""By default, relative paths are prefixed with './' when
-0/--print0 is given, to reduce the risk of a
path starting with '-' being treated as a command line option. Use
this flag to change this behavior."""
        )
        parser.add_argument(
            "--one-file-system",
            action="store_true",
            help=
"""By default, fd will traverse the file system tree as far as other options
dictate. With this flag, fd ensures that it does not descend into a
different file system than the one it started in. Comparable to the -mount
or -xdev filters of find(1)."""
        )

        self.args = parser.parse_args()

    def search_paths(self) -> list[pathlib.Path]:
        # would it make sense to concatenate these?
        if self.path:
            paths = self.path
        elif self.search_path:
            paths = self.search_path
        else:
            return [pathlib.Path('.')]

        def path_is_valid(path):
            if path.is_dir():
                return True
            else:
                from .error import print_error

                print_error("Search path '%s' is not a directory." % path)
                return False

        return list(filter(path_is_valid, paths))

    def rg_alias_ignore(self):
        return self.rg_alias_hidden_ignore > 0

    def strip_cwd_prefix(self, auto_pred: Callable) -> bool:
        if self.no_search_paths():
            if self._strip_cwd_prefix:
                return True
            else:
                return auto_pred()
        else:
            return False

    def no_search_paths(self) -> bool:
        return not self.path and not self.search_path

    def max_results(self) -> int | None:
        if self._max_results and self._max_results > 0:
            return self._max_results
        elif self._max_one_result:
            return 1
        else:
            return None

    def max_depth(self) -> int | None:
        if self._max_depth:
            return self._max_depth
        elif self.exact_depth:
            return self.exact_depth
        else:
            return None

    def min_depth(self) -> int | None:
        if self._min_depth:
            return self._min_depth
        elif self.exact_depth:
            return self.exact_depth
        else:
            return None

    def __getattr__(self, name):
        return self.args.__getattribute__(name)

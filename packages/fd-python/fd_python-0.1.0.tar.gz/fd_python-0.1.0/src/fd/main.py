import os
import pathlib
import regex
import sys

from . import exit_codes
from .cli import Opts
from .config import Config
from .regex_helper import pattern_has_uppercase_char, pattern_matches_strings_with_leading_dot
from .walk import scan


def main() -> int:
    try:
        sys.exit(run())
    except Exception as e:
        from .error import print_error

        print_error(e)

        sys.exit(exit_codes.GENERAL_ERROR)


def run() -> int:
    opts: Opts = Opts.parse()

    # TODO(cplrossi): shell completion

    set_working_dir(opts)
    search_paths: list[pathlib.Path] = opts.search_paths()

    if not search_paths:
        raise Exception("No valid search paths given.")

    ensure_search_pattern_is_not_a_path(opts)

    exprs: list[str] = opts.exprs if opts.exprs else []
    exprs.append(opts.pattern)

    pattern_regexes: list[str] = [build_pattern_regex(pat, opts) for pat in exprs]

    config: Config = construct_config(opts, pattern_regexes)

    ensure_use_hidden_option_for_leading_dot_pattern(config, pattern_regexes)

    regexes: list[regex.Pattern] = [build_regex(pat, config) for pat in pattern_regexes]

    return scan(search_paths, regexes, config)


def set_working_dir(opts):
    if opts.base_directory is not None:
        if not opts.base_directory.is_dir():
            raise Exception("The '--base-directory' path '%s' is not a directory." % opts.base_directory)

        os.chdir(opts.base_directory)


def ensure_search_pattern_is_not_a_path(opts):
    if not opts.full_path and \
       os.sep in opts.pattern and \
       pathlib.Path(opts.pattern).is_dir():
        raise Exception("The search pattern '{pattern}' contains a path-separation character ('{sep}') "
                        "and will not lead to any search results.\n\n"
                        "If you want to search for all files inside the '{pattern}' directory, use a match-all pattern:\n\n  "
                        "fd . '{pattern}'\n\n"
                        "Instead, if you want your pattern to match the full file path, use:\n\n  "
                        "fd --full-path '{pattern}'".format(pattern=opts.pattern, sep=os.sep)
        )


def build_pattern_regex(pattern: str, opts: Opts):
    if opts.glob and not opts.regex and pattern:
        from wcmatch import glob

        reg = glob.translate(pattern)

        return reg[0][0]
    elif opts.fixed_strings:
        return regex.escape(pattern)
    else:
        return pattern


def construct_config(opts: Opts, pattern_regexes: list[str]) -> Config:
    # The search will be case-sensitive if the command line flag is set or
    # if any of the patterns has an uppercase character (smart case).
    case_sensitive = not opts.ignore_case and \
        (opts.case_sensitive or \
         any([pattern_has_uppercase_char(pat) for pat in pattern_regexes]))

    path_separator: str | None = opts.path_separator
    actual_path_separator: str = path_separator if path_separator else os.sep

    check_path_separator_length(path_separator)

    size_limits = opts.size

    return Config(
        case_sensitive=case_sensitive,
        search_full_path=opts.full_path,
        ignore_hidden=not (opts.hidden or opts.rg_alias_ignore()),
        read_fdignore=not (opts.no_ignore or opts.rg_alias_ignore()),
        read_vcsignore=not (opts.no_ignore or opts.rg_alias_ignore() or opts.no_ignore_vcs),
        require_git_to_read_vcsignore=not opts.no_require_git,
        read_parent_ignore=not opts.no_ignore_parent,
        follow_links=opts.follow,
        one_file_system=opts.one_file_system,
        null_separator=opts.null_separator,
        quiet=opts.quiet,
        max_depth=opts.max_depth(),
        min_depth=opts.min_depth(),
        exclude_patterns=list(map(lambda p: "!" + p, opts.exclude)),
        ignore_files=opts.ignore_file,
        size_constraints=size_limits,
        show_filesystem_errors=opts.show_errors,
        path_separator=path_separator,
        actual_path_separator=actual_path_separator,
        max_results=opts.max_results(),
        strip_cwd_prefix=opts.strip_cwd_prefix(lambda: not opts.null_separator),
    )


def check_path_separator_length(path_separator: str | None):
    if path_separator and os.name == "nt":
        sep_len = len(path_separator.encode("utf-8"))

        if sep_len > 1:
            raise Exception("A path separator must be exactly one byte, but "
                            "the given separator is %u bytes: '%s'.\n"
                            "In some shells on Windows, '/' is automatically "
                            "expanded. Try to use '//' instead." % (sep_len, path_separator))


def ensure_use_hidden_option_for_leading_dot_pattern(config: Config, pattern_regexes: list[str]):
    if os.name == "posix" and \
       config.ignore_hidden and \
       any([pattern_matches_strings_with_leading_dot(pat) for pat in pattern_regexes]):
        raise Exception("The pattern(s) seems to only match files with a leading dot, but hidden files are "
                        "filtered by default. Consider adding -H/--hidden to search hidden files as well "
                        "or adjust your search pattern(s).")


def build_regex(pattern_regex, config) -> regex.Pattern:
    flags = regex.DOTALL

    if not config.case_sensitive:
        flags |= regex.IGNORECASE

    try:
        return regex.compile(pattern_regex, flags)
    except Exception as e:
        raise Exception("%s\n\nNote: You can use the '--fixed-strings' option to search for a "
                        "literal string instead of a regular expression. Alternatively, you can "
                        "also use the '--glob' option to match on a glob pattern." % e)

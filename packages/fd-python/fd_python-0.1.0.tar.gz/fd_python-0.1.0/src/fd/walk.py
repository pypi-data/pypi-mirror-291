from dataclasses import dataclass
import errno
import ignore
from ignore import WalkBuilder
from ignore.overrides import OverrideBuilder, Override
import os
import pathlib
import regex
import signal
import sys

from . import exit_codes
from .config import Config
from .dir_entry import DirEntry
from .error import print_error
from .output import print_entry


@dataclass
class WorkerState:
    patterns: list[regex.Pattern]
    config: Config
    num_results: int = 0

    def build_overrides(self, paths) -> Override:
        first_path = paths[0]

        builder = OverrideBuilder(first_path)

        for pattern in self.config.exclude_patterns:
            try:
                builder.add(pattern)
            except Exception as e:
                raise Exception("Malformed exclude pattern: %s" % e)

        try:
            return builder.build()
        except:
            raise Exception("Mismatch in exclude patterns")

    def build_walker(self, paths: list[pathlib.Path]) -> ignore.Walk:
        first_path: pathlib.Path = paths[0]
        config = self.config
        overrides = self.build_overrides(paths)

        builder = WalkBuilder(first_path)
        (builder
         .hidden(config.ignore_hidden)
         .ignore(config.read_fdignore)
         .parents(config.read_parent_ignore and (config.read_fdignore or config.read_vcsignore))
         .git_ignore(config.read_vcsignore)
         .git_global(config.read_vcsignore)
         .git_exclude(config.read_vcsignore)
         .require_git(config.require_git_to_read_vcsignore)
         .overrides(overrides)
         .follow_links(config.follow_links)
         .same_file_system(config.one_file_system)
         .max_depth(config.max_depth))

        if config.read_fdignore:
            builder.add_custom_ignore_filename(".fdignore")

        for ignore_file in config.ignore_files:
            try:
                builder.add_ignore(ignore_file)
            except Exception as e:
                from .error import print_error

                print_error("Malformed pattern in custom ignore file. %s." % e)

        for path in paths[1:]:
            builder.add(path)

        walker = builder.build()

        return walker

    def scan(self, paths: list[pathlib.Path]) -> int:
        walker = self.build_walker(paths)

        signal.signal(signal.SIGINT, lambda _, __: sys.exit(exit_codes.KILLED_BY_SIGINT))

        while True:
            try:
                ignore_entry: ignore.DirEntry = next(walker)

                if ignore_entry.depth() == 0:
                    # Skip the root directory entry.
                    continue

                entry: DirEntry = DirEntry.normal(ignore_entry)
            except StopIteration:
                break
            except ignore.IOError as e:
                if e.errno == errno.ENOENT:
                    path = pathlib.Path(e.filename)

                    if path.is_symlink():
                        entry: DirEntry = DirEntry.broken_symlink(path)
                    else:
                        continue
                else:
                    if self.config.show_filesystem_errors:
                        print_error(e)

                    continue
            except Exception as e:
                if self.config.show_filesystem_errors:
                    print_error(e)
                continue

            if self.config.min_depth:
                if entry.depth() < self.config.min_depth:
                    continue

            entry_path: pathlib.Path = entry.path()

            search_str = entry_path.resolve() if self.config.search_full_path else entry_path.name

            if not all(map(lambda pat: pat.match(str(search_str)), self.patterns)):
                continue

            # Filter out unwanted sizes if it is a file and we have been given size constraints.
            if self.config.size_constraints:
                if entry_path.is_file():
                    stat: os.stat_result = entry.stat()

                    file_size = stat.st_size

                    if any(map(lambda sc: not sc.is_within(file_size), self.config.size_constraints)):
                        continue
                else:
                    continue

            self.num_results += 1

            if self.config.quiet:
                return exit_codes.HAS_RESULTS

            self.print(entry)

            if self.config.max_results and self.num_results >= self.config.max_results:
                return self.stop()

        return self.stop()

    def stop(self):
        if self.config.quiet:
            return exit_codes.HAS_RESULTS if self.num_results > 0 else exit_codes.NOT_HAS_RESULTS

        return exit_codes.SUCCESS

    def print(self, entry):
        print_entry(entry, self.config)


def scan(paths: list[pathlib.Path], patterns: list[regex.Pattern], config: Config) -> int:
    return WorkerState(patterns, config).scan(paths)

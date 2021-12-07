# Copyright 2021 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Representations specific to the SHARC compiler families."""

import os
import typing as T

from ...mesonlib import EnvironmentException

if T.TYPE_CHECKING:
    from ...environment import Environment
    from ...compilers.compilers import Compiler
else:
    # This is a bit clever, for mypy we pretend that these mixins descend from
    # Compiler, so we get all of the methods and attributes defined for us, but
    # for runtime we make them descend from object (which all classes normally
    # do). This gives up DRYer type checking, with no runtime impact
    Compiler = object

sharc_buildtype_args = {
    'plain': [''],
    'debug': ['-O0', '-g'],
    'debugoptimized': ['-O0', '-g'],
    'release': ['-03'],
    'minsize': ['-Os'],
    'custom': [],
}  # type: T.Dict[str, T.List[str]]

sharc_optimization_args = {
    '0': ['-O0'],
    'g': ['-O0'],
    '1': ['-O1'],
    '2': ['-O2'],
    '3': ['-O3'],
    's': ['-Os']
}  # type: T.Dict[str, T.List[str]]

sharc_debug_args = {
    False: [],
    True: ['-g']
}  # type: T.Dict[bool, T.List[str]]

class SharcCompiler(Compiler):

    def __init__(self) -> None:
        if not self.is_cross:
            raise EnvironmentException('c2000 supports only cross-compilation.')
        self.id = 'sharc'
        default_warn_args = []  # type: T.List[str]
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args + [],
                          '3': default_warn_args + []}  # type: T.Dict[str, T.List[str]]

    def get_pic_args(self) -> T.List[str]:
        # Sharc does not support PIC
        return []

    def get_buildtype_args(self, buildtype: str) -> T.List[str]:
        return sharc_buildtype_args[buildtype]

    def get_pch_suffix(self) -> str:
        return 'pch'

    def get_pch_use_args(self, pch_dir: str, header: str) -> T.List[str]:
        return []

    def thread_flags(self, env: 'Environment') -> T.List[str]:
        return []

    def get_coverage_args(self) -> T.List[str]:
        return []

    def get_no_stdinc_args(self) -> T.List[str]:
        return ['-no-std-inc']

    def get_no_stdlib_link_args(self) -> T.List[str]:
        return ['-no-std-lib']

    def get_optimization_args(self, optimization_level: str) -> T.List[str]:
        return sharc_optimization_args[optimization_level]

    def get_debug_args(self, is_debug: bool) -> T.List[str]:
        return sharc_debug_args[is_debug]

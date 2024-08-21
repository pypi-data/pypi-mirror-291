# Copyright (C) 2024 Lucas Hinderberger
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers and utilities for dealing with metadata."""

from typing import override

from thoughtwrapper import Dependencies, Filter, Stage

__all__ = ["Injector"]


class Injector(Filter):
    """A thoughtwrapper Filter that adds user-defined metadata."""

    def __init__(self, metadata: dict, dependencies: Dependencies):
        """Create a new Injector.

        The arguments will be used to initialize instance properties of
        the same name.

        :param metadata: The metadata that is to be added to the
            existing metadata using dict.update(). Note that the new
            metadata will thus be shallowly merged into the old metadata.
        :param dependencies: Indicate if the new metadata can change
            and/or depends on files on disk. If the metadata cannot
            change during or across build script runs (e.g. a constant
            dict), pass in an empty list. If it can change, but only
            depending on the contents of certain files on disk, pass in
            a list of filenames. If it can change dynamically, e.g. by
            environment variable or network request, pass in None.
        """
        self.metadata = metadata
        self.dependencies = dependencies

    @override
    def stages(self) -> list[Stage]:
        """Override stages method of Filter."""
        return [Stage.METADATA]

    @override
    def filter_metadata(self, raw: bytes, metadata: dict) -> Dependencies:
        """Override filter_metadata method of Filter."""
        metadata.update(self.metadata)
        return self.dependencies

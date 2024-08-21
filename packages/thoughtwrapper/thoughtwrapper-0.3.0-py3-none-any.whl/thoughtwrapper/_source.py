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

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self, override


class Dependencies:
    """Identifies the build dependencies of a route.

    Dependencies points to files on disk that are necessary for building
    a particular route. It is useful for cache invalidation, when
    combined with watching disk operations.

    Dependencies can also have a "dynamic" flag set, indicating that the
    route depends on dynamic, nondeterministic input, for example
    webservice queries. Thus, the pipeline's results should not be
    cached.
    """

    def __init__(self, *args: str | os.PathLike, dynamic: bool = False):
        """Create a new Dependencies list.

        :param args: A full or partial set of filenames that a route
            depends on. This will be used to initialize an instance
            property of the name filenames, which is of type set.
            The paths will be resolved before initializing that set.
        :param dynamic: Set this to true if the route depends on dynamic
            input. This will be used to initialize an instance property
            of the same name.

        See class description for details on parameter semantics.
        """
        self.dynamic = dynamic
        self.filenames = {str(Path(a).resolve()) for a in args}

        if not all(isinstance(x, str) for x in self.filenames):
            raise RuntimeError(
                "encountered Dependency list with non-string value(s)",
            )

    def __eq__(self, other: Self):
        """Test for equality."""
        return (
            self.dynamic == other.dynamic
            and self.filenames == other.filenames
        )

    def __repr__(self):
        """Build string representation."""
        params = [x.__repr__() for x in self.filenames]
        params += [f"dynamic={self.dynamic}"]
        return f"Dependencies({', '.join(params)})"

    def clear(self):
        """Clear this instance.

        The instance will be reset to a state as if it was initialized
        with an empty constructor call.
        """
        self.filenames.clear()
        self.dynamic = False

    def update(self, other: Self):
        """Update this list of Dependencies by merging the other one.

        Duplicate filenames will be omitted (if they equal each other as
        strings). If the other instance has its "dynamic" flag set, the
        "dynamic" flag of this instance will also be set.
        """
        self.filenames.update(other.filenames)

        if other.dynamic:
            self.dynamic = True


class Source(ABC):
    """A source of input to a Pipeline (abstract base class)."""

    @abstractmethod
    def read(self, metadata: dict) -> tuple[bytes, Dependencies]:
        """Read the Source to a byte array.

        :param metadata: Metadata about the Source (e.g. modification
            time) can be added to the given metadata dictionary.
        """
        raise RuntimeError("not implemented")


class BytesSource(Source):
    """BytesSource is a Source that returns a user-defined byte array."""

    def __init__(self, data: bytes, deps: Dependencies):
        """Create a new BytesSource.

        The arguments will be used to initialize instance properties of
        the same name.

        :param data: The byte array that shall be used as source.
        :param deps: Indicates what Dependencies were necessary for
            building the byte array.
        """
        self.data = data
        self.deps = deps

    @override
    def read(self, metadata: dict) -> tuple[bytes, Dependencies]:
        """Override Source's read method."""
        return self.data, self.deps


class FileSource(Source):
    """FileSource is a Source that returns the contents of a file on disk."""

    def __init__(self, filepath: str | os.PathLike):
        """Create a new FileSource.

        :param filepath: The path of the file on disk that shall be used
            as source. This will be used to initialize an instance
            property of the same name.
        """
        self.filepath = filepath

    @override
    def read(self, metadata: dict) -> tuple[bytes, Dependencies]:
        """Override Source's read method."""
        resolved_path = Path(self.filepath).resolve()
        metadata["_tw"]["filepath"] = resolved_path
        metadata["_tw"]["filestat"] = resolved_path.stat()
        with Path(self.filepath).open("rb") as f:
            return f.read(), Dependencies(resolved_path)


class StringSource(Source):
    """StringSource is a Source that returns a user-defined string."""

    def __init__(self, data: str, deps: Dependencies, encoding: str = "UTF-8"):
        """Create a new StringSource.

        The arguments will be used to initialize instance properties of
        the same name.

        :param data: The string that shall be used as source.
        :param deps: Indicates what Dependencies were necessary for
            building the byte array.
        :param encoding: The encoding that shall be used for turning the
            string into a byte array.
        """
        self.data = data
        self.deps = deps
        self.encoding = encoding

    @override
    def read(self, metadata: dict) -> tuple[bytes, Dependencies]:
        """Override Source's read method."""
        return self.data.encode(encoding=self.encoding), self.deps

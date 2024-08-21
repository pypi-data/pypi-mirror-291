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

"""Loading metadata from file headers (the so-called front matter)."""

import tomllib
from typing import override

from thoughtwrapper import Dependencies, Filter, Stage

__all__ = ["Loader"]


class Loader(Filter):
    """A thoughtwrapper Filter for loading metadata from front matter.

    So-called front matter are file headers prepended to e.g. a template
    and separated from the content by a separator line.

    The metadata in the front matter is encoded in a data serialization
    format - for this Filter, TOML is used.
    """

    def __init__(
        self,
        separator_line: str = "---",
        input_encoding: str = "UTF-8",
        output_encoding: str = "UTF-8",
    ):
        """Create a new front matter loader Filter.

        The metadata loaded by this Filter will be merged with the
        already existing metadata using dict.update().

        The arguments will be used to initialize instance properties of
        the same name.

        :param separator_line: The expected contents of the line that
            that separates front matter and content. Note that trailing
            whitespace will be ignored when searching for the separator
            line.
        :param input_encoding: The encoding that is used for reading
            input bytes to string.
        :param output_encoding: The encoding that is used for writing
            filter_raw output back to bytes.
        """
        self.separator_line = separator_line
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding

    @override
    def stages(self) -> list[Stage]:
        """Override stages method of Filter."""
        return [Stage.METADATA, Stage.RAW]

    @override
    def filter_metadata(self, raw: bytes, metadata: dict) -> Dependencies:
        """Override filter_metadata method of Filter."""
        frontmatter_toml, _ = self.split(raw)

        try:
            frontmatter = tomllib.loads(frontmatter_toml)
        except Exception as e:
            raise RuntimeError("Error while parsing front matter") from e

        metadata.update(frontmatter)

        return Dependencies()

    @override
    def filter_raw(
        self, raw: bytes, metadata: dict,
    ) -> tuple[bytes, Dependencies]:
        """Override filter_raw method of Filter."""
        _, content = self.split(raw)
        return (content.encode(encoding=self.output_encoding), Dependencies())

    def split(self, raw: bytes) -> tuple[str, str]:
        """Split raw input into front matter and content.

        This function's output does not contain the separator line.
        """
        input_str = str(raw, encoding=self.input_encoding)
        input_lines = input_str.splitlines(keepends=True)

        # Find index of separator line
        separator_idx = next(
            (
                i for (i, v) in enumerate(input_lines)
                if v.rstrip() == self.separator_line
            ),
            None,  # if no separator line is found, set the index to None
        )

        if separator_idx is None:
            return ("", input_str)

        frontmatter_lines = input_lines[0:separator_idx]
        content_lines = input_lines[separator_idx+1:]

        return ("".join(frontmatter_lines), "".join(content_lines))

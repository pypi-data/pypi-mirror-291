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

"""Rendering Markdown / CommonMark documents using the Marko library."""

from typing import override

import marko

from thoughtwrapper import Dependencies, Filter, Stage

__all__ = ["Renderer"]


class Renderer(Filter):
    """A thoughtwrapper Filter for rendering Markdown / CommonMark documents.

    This filter uses the Marko library as its rendering engine. The
    marko.Markdown class is exposed to ensure maximum configurability.
    """

    def __init__(
        self,
        md: marko.Markdown = None,
        input_encoding: str = "UTF-8",
        output_encoding: str = "UTF-8",
    ):
        """Create a new Filter for rendering Markdown / Commonmark documents.

        The arguments will be used to initialize instance properties of
        the same name.

        :param md: A custom marko.Markdown instance to use for parsing
            and rendering the document. If not specified, an instance in
            default configuration will be used.
        :param input_encoding: The encoding that is used for template
            sources (raw bytes input).
        :param output_encoding: The encoding that will be used for
            coverting the template output to bytes.
        """
        if md is None:
            md = marko.Markdown()

        self.md = md
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding

    @override
    def stages(self) -> list[Stage]:
        """Override stages method of Filter."""
        return [Stage.RAW]

    @override
    def filter_raw(
        self, raw: bytes, metadata: dict,
    ) -> tuple[bytes, Dependencies]:
        """Override filter_raw method of Filter."""
        decoded_raw = raw.decode(self.input_encoding)
        out = self.md.convert(decoded_raw)
        return (bytes(out, self.output_encoding), Dependencies())

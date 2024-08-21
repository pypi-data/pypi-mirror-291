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

"""Syntax highlighting within HTML code blocks using the Pygments library."""

import itertools
import logging
from typing import override

import bs4
from pygments import highlight
from pygments.formatter import Formatter
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from thoughtwrapper import Dependencies, Filter, Stage

__all__ = ["Highlighter"]


class Highlighter(Filter):
    """A thoughtwrapper Filter for highlighting syntax within a HTML document.

    Code blocks are selected from the DOM using the BeautifulSoup library and
    are then passed to the Pygments library for syntax highlighting. The output
    of Pygments is then used to replace the contents of the corresponding code
    blocks.

    To fine-tune code block selection / code and language extraction, subclass
    Highlighter and override the corresponding methods.
    """

    def __init__(self, formatter: Formatter | None = None):
        """Create a new syntax highlighting Filter.

        :param formatter: By default, this filter uses an HtmlFormatter
            with the nowrap function for highlighting syntax using
            Pygments. You can override this by passing in a custom
            formatter. This will be used to initialize an instance
            property of the same name.
        """
        if formatter is None:
            formatter = HtmlFormatter(nowrap=True)

        self.formatter = formatter

    @override
    def stages(self) -> list[Stage]:
        """Override stages method of Filter."""
        return [Stage.HTML]

    @override
    def filter_html(
        self, dom: bs4.BeautifulSoup, metadata: dict,
    ) -> Dependencies:
        """Override filter_html method of Filter."""
        code_blocks = self.select_block(dom)

        if len(code_blocks) == 0:
            logging.debug("no code blocks found")

        for block in code_blocks:
            code = self.extract_code(block)
            language = self.extract_lang(block)

            block_path = "/".join(itertools.chain(
                reversed([p.name for p in block.parents]),
                [block.name],
            ))

            block_location = (
                f"(original) line {block.sourceline}, "
                f"column {block.sourcepos}, "
                f"path {block_path}"
            )

            logging.debug("processing code block at %s", block_location)

            if language is None:
                logging.warning(
                    "code block at %s has no language name - skipping",
                    block_location,
                )
                continue

            logging.debug('extracted language name "%s"', language)

            lexer = None
            try:
                lexer = get_lexer_by_name(language)
            except ClassNotFound:
                logging.warning(
                    'could not find lexer for language "%s" - skipping',
                    language,
                )

                continue

            t_lexer = type(lexer)
            logging.debug(
                "found lexer: %s.%s",
                t_lexer.__module__, t_lexer.__name__,
            )

            # Note that the output of highlight is wrapped in a pre tag.
            # This is so that BeautifulSoup preserves whitespace while
            # parsing the new tag during block.append().
            # The pre tag is then stripped away again using .unwrap().
            code_hl = highlight(code, lexer, self.formatter)
            code_hl = f"<pre>{code_hl}</pre>"

            block.clear()
            block.append(bs4.BeautifulSoup(code_hl, "html.parser"))
            block.pre.unwrap()

        return Dependencies()

    def select_block(self, dom: bs4.BeautifulSoup) -> list[bs4.PageElement]:
        """Select all blocks of code from a given DOM tree.

        This is the default selector function, which selects all "code"
        HTML tags.
        """
        return dom.find_all("code")

    def extract_code(self, element: bs4.PageElement) -> str:
        """Extract code from a code block element.

        This function is used to extract the raw source code (which is
        later passed to the syntax highlighting library) from a given
        code block.

        This is the default extractor function, which simply returns the
        code block's text contents and discards any tags that may be
        present in the input.
        """
        return element.get_text()

    def extract_lang(self, element: bs4.PageElement) -> str | None:
        """Try to extract language name from a code block element.

        This is used to determine what language's syntax should be used
        for highlighting.

        This is the default extractor function, which tries to extract the
        language provided via a "language-XYZ" class on an HTML tag.
        """
        prefix = "language-"

        classes = element.attrs.get("class")
        if classes is not None:
            if isinstance(classes, str):
                classes = [classes]

            for c in element.attrs["class"]:
                if c.startswith(prefix):
                    return c.removeprefix(prefix)

        return None

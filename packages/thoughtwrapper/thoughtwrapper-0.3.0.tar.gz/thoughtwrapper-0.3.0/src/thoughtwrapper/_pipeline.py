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

import logging
from enum import IntEnum

from bs4 import BeautifulSoup

from ._source import Dependencies, Source


class Stage(IntEnum):
    """Enumerates all Filter stages, in order of execution.

    The following stages are available, and are executed in the
    following order:

    - METADATA: Collection and transformation of metadata

    - RAW: Transformation of raw data
        At this stage, there is no DOM tree or similar. Input and output
        are read from/to byte arrays.

        This stage is intended for preprocessing a route's content
        before and up to the point it becomes a full HTML document, or
        for processing of binary / other non-HTML data.

    - HTML: Transformation of an HTML DOM
        The DOM is built from the final output of the raw filter stage.

        DOM contents can be modified and will be serialized at the end
        of the Pipeline run.
    """

    METADATA = 10
    RAW = 20
    HTML = 30


class StageNotSupportedError(Exception):
    """Indicates that an unsupported Filter stage was attempted to be run."""

    def __init__(self, stage: Stage):
        """Create a new StageNotSupportedError."""
        super().__init__(
            f"Attempted to run unsupported Filter stage: {stage}",
        )


class Filter:
    """Transforms the content and metadata of a route.

    This is a base class for all filters.

    Filters are usually applied in a :class:`Pipeline`, please refer
    to its documentation for details on Pipeline execution.

    The available filter stages are described at :class:`Stage`.

    Each filter stage matches one of the filter_* methods of this class.
    Your filter class should override the corresponding method(s) for
    the stage(s) you want to implement, and also override :meth:`stages`
    to declare which stages your Filter implements.
    """

    def stages(self) -> list[Stage]:
        """Declare which stages are supported by this Filter."""
        return []

    def filter_metadata(
        self, raw: bytes, metadata: dict,  # noqa: ARG002
    ) -> Dependencies:
        """Transform metadata."""
        raise StageNotSupportedError(Stage.METADATA)

    def filter_raw(
        self, raw: bytes, metadata: dict,  # noqa: ARG002
    ) -> tuple[bytes, Dependencies]:
        """Transform raw data."""
        raise StageNotSupportedError(Stage.RAW)

    def filter_html(
        self, dom: BeautifulSoup, metadata: dict,  # noqa: ARG002
    ) -> Dependencies:
        """Transform an HTML DOM."""
        raise StageNotSupportedError(Stage.HTML)


class Pipeline:
    """Manages and executes a pipeline filters for rendering content.

    A Pipeline is executed before rendering a route's contents. When
    executing a Pipeline, the original content is read and then passed
    through and transformed by a series of filters, as configured in the
    Pipeline.

    There are multiple filter stages that will be executed in sequence.
    Each filter stage is executed entirely (meaning all filters in that
    stage will run) before moving on to the next stage.

    The available filter stages and their order are described at
    :class:`Stage`.
    Note that a Pipeline stage is only executed if at least one
    corresponding Filter was added to the Pipeline. In particular, the
    HTML DOM is only built if HTML DOM filters are configured.

    During each Pipeline run, a metadata dictionary is created and
    maintained, containing information added by the filters along the
    way (e.g. front matter, or file metadata) for use by other filters
    further down the Pipeline.
    """

    def __init__(self, html_output_encoding: str = "utf-8"):
        """Create a new Pipeline.

        :param html_output_encoding: The encoding to use for turning the
            output of the HTML filter stage (if any) back to bytes. This
            also applies to the output of HTML prettification. This will
            be used to initialize an instance property of the same name.

        The filters are stored in an instance property by the name of
        filters.
        """
        self.filters = []
        self.html_output_encoding = html_output_encoding

        self._all_stages = [
            (Stage.METADATA, self._run_metadata),
            (Stage.RAW, self._run_raw),
            (Stage.HTML, self._run_html),
        ]

    def add_filter(self, filter_: Filter):
        """Append a Filter to the Pipeline."""
        self.filters.append(filter_)

    def add_filters(self, filters: list[Filter]):
        """Append multiple Filters to the Pipeline, in the given order."""
        self.filters += filters

    def run(
        self,
        source: Source,
        until_stage: Stage | None = None,
        metadata: dict | None = None,
    ) -> tuple[bytes, Dependencies]:
        """Execute the Pipeline for a single source.

        This function is primarily for internal use. You are probably
        looking for the Site class instead.

        :param source: The input to the Pipeline.
        :param until_stage: If specified, the Pipeline will only be
            executed up to and including the given filter stage.
            Otherwise the entire Pipeline will be executed.
        :param metadata: If specified, the metadata dictionary that the
            pipeline shall operate on. If None, a new dictionary will be
            initialized with {"_tw": {}}.

        Returns a tuple of the output bytes, metadata dictionary and
        Dependencies of this pipeline run.
        """
        logging.debug("running Pipeline")

        if metadata is None:
            metadata = {"_tw": {}}
        out, deps = source.read(metadata)

        if until_stage is None:
            logging.debug("no stage was set, defaulting to HTML")
            until_stage = Stage.HTML

        for stage, runfunc in self._all_stages:
            if stage <= until_stage:
                logging.debug("entering stage %s", stage.name)
                out, metadata, deps = runfunc(out, metadata, deps)

        logging.debug("determined dependencies for route: %s", deps)

        return (out, deps)

    def _run_metadata(
        self, out: bytes, metadata: dict, deps: Dependencies,
    ) -> tuple[bytes, dict, Dependencies]:
        for f in self.filters:
            if Stage.METADATA in f.stages():
                _log_running_filter(f)
                more_deps = f.filter_metadata(out, metadata)
                deps.update(more_deps)

        return (out, metadata, deps)

    def _run_raw(
        self, out: bytes, metadata: dict, deps: Dependencies,
    ) -> tuple[bytes, dict, Dependencies]:
        for f in self.filters:
            if Stage.RAW in f.stages():
                _log_running_filter(f)
                out, more_deps = f.filter_raw(out, metadata)
                deps.update(more_deps)

        return (out, metadata, deps)

    def _run_html(
        self, out: bytes, metadata: dict, deps: Dependencies,
    ) -> tuple[bytes, dict, Dependencies]:
        dom = None

        for f in self.filters:
            if Stage.HTML in f.stages():
                _log_running_filter(f)
                if dom is None:
                    dom = BeautifulSoup(out, "html.parser")
                more_deps = f.filter_html(dom, metadata)
                deps.update(more_deps)

        if dom is not None:
            out = str(dom).encode(self.html_output_encoding)

        return (out, metadata, deps)


def _log_running_filter(f: Filter):
    t_f = type(f)
    logging.debug("running Filter %s.%s", t_f.__module__, t_f.__name__)

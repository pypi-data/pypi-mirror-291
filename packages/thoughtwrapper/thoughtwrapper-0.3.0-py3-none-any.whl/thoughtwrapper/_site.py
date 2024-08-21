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
import os
import time
from pathlib import Path
from typing import BinaryIO

from ._pipeline import Pipeline
from ._source import FileSource, Source
from ._util import open_output as _open_output


class InvalidPathError(Exception):
    """InvalidPathError indicates that a URL path was found to be invalid."""

class RouteNotFoundError(Exception):
    """RouteNotFoundError indicates that a requested route was not found."""


class Site:
    """Holds the build configuration and state for a thoughtwrapper site.

    A site is composed of routes, accessible by their URL path, which
    are stored in a Site instance's routes dict.
    """

    def __init__(self):
        """Create a new Site.

        Under attribute name routes, Site holds a dictionary, where each
        Route in the site is indexed by its URL path.
        """
        self.routes: dict[str, Route] = {}

    def add_route(
        self,
        pipeline: Pipeline, url_path: str | os.PathLike,
        source: Source | str | os.PathLike,
    ):
        """Create and add a new route to the build configuration.

        If route points to an existing route, that existing route will
        be overwritten.

        If you have an existing Route instance, you can add it to the
        routes dict directly instead of calling add_route.

        :param pipeline: The pipeline that shall be executed for this
            route.
        :param url_path: The URL path of the new route. It is cleaned
            using the clean_url_path function before being added to the
            routes dictionary. For easier route construction, a
            path-like object may be passed in, which will be converted
            to string internally.
        :param source: The source of the content that is to be rendered
            to the given route. If a string or PathLike is given, it
            will be used to initialize a new :class:`FileSource`.
        """
        url_path = clean_url_path(url_path)

        if isinstance(source, os.PathLike | str):
            source = FileSource(source)

        self.routes[url_path] = Route(url_path, pipeline, source)

    def add_routes(
        self,
        pipeline: Pipeline,
        routes: dict[str | os.PathLike, Source | str | os.PathLike],
    ):
        """Create and add multiple routes to the build configuration.

        If you have existing Route instances, you can add them to the
        routes dict directly instead of calling add_routes.

        :param pipeline: The pipeline that shall be executed for all
            given routes.
        :param routes: A dictionary of sources, keyed by route URL path.
            For more details, refer to the documentation of
            :meth:`add_route`.
        """
        for route, source in routes.items():
            self.add_route(pipeline, route, source)

    def build(self, output_path: str | os.PathLike):
        """Build the entire site to output_path."""
        output_path = Path(output_path)

        for url_path, route in self.routes.items():
            route_output_path = output_path.joinpath(url_path)
            with _open_output(route_output_path) as output:
                output.write(route.build())

    def build_single(self, route_urlpath: str, output: BinaryIO):
        """Build a single route and write to the given output."""
        try:
            entry = self.routes[route_urlpath]
        except KeyError as e:
            raise RouteNotFoundError(
                f"Route not found: {route_urlpath}",
            ) from e

        output.write(entry.build())


class Route:
    """Holds the build configuration and state for a single route.

    Each route has a source and is handled by a pipeline, which are both
    configured within Route. The URL path is stored redundantly to
    Site's routes dictionary.

    Build state, namely Dependencies and a timestamp of when the route
    was last built is stored in the "dependencies" and "last_build_at"
    attributes.

    The build output is cached in the "cached_output" attribute (unless
    the route's Dependencies have the "dynamic" flag set). The cache
    will be invalidated if any of the Dependencies is modified after the
    route was last built (as determined by the file's modification
    timestamp).
    """

    def __init__(self, url_path: str, pipeline: Pipeline, source: Source):
        """Create a new _Route."""
        self.url_path = url_path
        self.pipeline = pipeline
        self.source = source

        self.dependencies = None
        self.last_built_at = None
        self.cached_output = None

    def build(self) -> bytes:
        """Build this route, update build metadata properties."""
        try:
            logging.info("Building route %s", self.url_path)
            if self.last_built_at is not None:
                logging.debug(
                    "route %s was last built at: %f",
                    self.url_path, self.last_built_at,
                )

            if not self.is_cache_stale():
                logging.debug(
                    "Returning cached contents for route %s",
                    self.url_path,
                )
                return self.cached_output

            # last_built_at is set before the build, so that the build cache
            # can be invalidated in case the input files change during the
            # build.
            self.last_built_at = time.time()

            logging.debug(
                "new last_built_at for route %s: %f",
                self.url_path, self.last_built_at,
            )
            metadata = {"_tw": {"url_path": self.url_path}}
            output, deps = self.pipeline.run(self.source, metadata=metadata)

            self.dependencies = deps
            self.cached_output = None if deps.dynamic else output

            return output
        except Exception as e:
            raise RuntimeError(f"Could not build route {self.url_path}") from e

    def is_cache_stale(self) -> bool:
        """Try to determine if the cached contents (if any) are stale."""
        if (
            self.cached_output is None
            or self.dependencies is None
            or self.dependencies.dynamic
        ):
            return True

        for filename in self.dependencies.filenames:
            mtime = Path(filename).stat().st_mtime
            logging.debug('mtime of "%s": %f', filename, mtime)
            if mtime > self.last_built_at:
                return True

        return False


def clean_url_path(url_path: str | os.PathLike) -> str:
    """Clean a URL path for use with `Site`.

    This function should not be used for general-purpose URL path
    cleaning, as it only performs some basic URL cleaning and
    practically no validation.
    """
    if isinstance(url_path, os.PathLike):
        url_path = str(url_path)

    parts = [p for p in url_path.split("/") if p not in ("", ".")]

    while ".." in parts:
        idx = parts.index("..")
        if idx == 0:
            raise InvalidPathError(
                "encountered URL path with top-level (or equivalent) "
                f'doubledot pattern: "{url_path}"',
            )

        del parts[idx-1:idx+1]

    if len(parts) == 0:
        raise InvalidPathError(f'path is empty (or equivalent): "{url_path}"')

    return "/".join(parts)

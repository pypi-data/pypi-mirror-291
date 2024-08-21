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

import http.server
import io
import logging
import mimetypes
from pathlib import PurePosixPath

from ._site import RouteNotFoundError, Site

DEFAULT_INDEX_FILENAMES = ["index.html", "index.htm"]
"""The default filenames that the dev server probes to find an index page."""


class DevServer(http.server.ThreadingHTTPServer):
    """An HTTP server for local authoring of a thoughtwrapper site."""

    def __init__(
        self,
        site: Site,
        listen_address: tuple[str, int],
        index_filenames: list[str] | None = None,
    ):
        """Create a new DevServer.

        :param site: The site for which to build a dev server.
        :param listen_address: The host and port under which the dev
            server shall listen for HTTP requests.
        :param index_filenames: Index filenames to try and append to
            routes that have no direct match. A path separator will be
            added automatically. If None, DEFAULT_INDEX_FILENAMES will
            be used.
        """
        if index_filenames is None:
            index_filenames = DEFAULT_INDEX_FILENAMES.copy()

        self.tw_index_filenames = index_filenames
        self.tw_site = site

        super().__init__(listen_address, _DevServerHandler)


class _DevServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        """Handle GET requests for thoughtwrapper dev server."""
        index_filenames = self.server.tw_index_filenames
        path = PurePosixPath(self.path.split("?", maxsplit=1)[0])

        routelist = [] if self.path.endswith("/") else [path]
        routelist += [path.joinpath(ifn) for ifn in index_filenames]

        routelist = [str(r).lstrip("/") for r in routelist]

        for route in routelist:
            with io.BytesIO() as f:
                try:
                    self.server.tw_site.build_single(route, f)
                except RouteNotFoundError:
                    continue
                except Exception as e:
                    # W0718 (broad-exception-caught) is suppressed because the
                    # dev server should not propagate any build exceptions out
                    # of request handlers. Instead, it should return error 500.
                    self.send_response(500)
                    self.end_headers()
                    logging.exception("Error building route")
                    self.wfile.write(str(e).encode("utf-8"))
                    return

                content_type, content_encoding = mimetypes.guess_type(route)
                if content_type is None:
                    content_type = "application/octet-stream"

                body = f.getvalue()

                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Encoding", content_encoding)
                self.send_header("Content-Length", len(body))
                self.end_headers()
                self.wfile.write(body)
                return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not Found")

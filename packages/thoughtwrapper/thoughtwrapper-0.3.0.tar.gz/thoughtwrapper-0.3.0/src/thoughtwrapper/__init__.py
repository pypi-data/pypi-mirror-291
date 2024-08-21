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

"""A Static Site Generator for Tinkerers."""

import argparse
import logging
import sys
from pathlib import Path

from ._devserver import DEFAULT_INDEX_FILENAMES, DevServer
from ._pipeline import Filter, Pipeline, Stage, StageNotSupportedError
from ._site import (
    InvalidPathError,
    Route,
    RouteNotFoundError,
    Site,
    clean_url_path,
)
from ._source import (
    BytesSource,
    Dependencies,
    FileSource,
    Source,
    StringSource,
)
from ._util import open_output as _open_output

__all__ = [
    "run",
    "DevServer", "DEFAULT_INDEX_FILENAMES",
    "Filter", "Pipeline", "Stage",
    "InvalidPathError", "Site", "Route", "RouteNotFoundError",
    "clean_url_path",
    "BytesSource", "Dependencies", "FileSource", "Source", "StringSource",
    "StageNotSupportedError",
]
__version__ = "0.3.0"


def run(site: Site, argv: list[str] | None = None):
    """Run the thoughtwrapper CLI for the given Site.

    This should be the last call in your site.py file, after
    setting up all routes.

    If no value is given for argv, the arguments to the current
    process (excluding binary path) will be used.
    """
    if argv is None:
        argv = sys.argv[1:]

    arg_parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="thoughtwrapper - "
                    "A Static Site Generator for Tinkerers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    arg_parser.add_argument(
        "-v", "--verbose",
        help="determines the logging level (DEBUG if not specified, otherwise "
             "INFO) - note that a build script may be able to override the "
             "log level",
        action="store_true",
    )

    subparsers = arg_parser.add_subparsers(
        title="COMMAND",
        dest="command",
        required=True,
    )

    build_parser = subparsers.add_parser(
        "build",
        help="builds your site (or parts thereof)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    build_parser.add_argument(
        "-o", "--output",
        help='output directory (or file, if --single is set), defaults '
             'to the "target" subdirectory of the current working '
             'directory (or stdout if --single is set)',
    )
    build_parser.add_argument(
        "-s", "--single",
        help="only build a single page, with the given URL path (outputs "
             "to stdout by default, override with --output)",
    )

    serve_parser = subparsers.add_parser(
        "serve",
        help="runs a development server for your site",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    serve_parser.add_argument(
        "--host",
        default="localhost",
        help="the host to listen to",
    )
    serve_parser.add_argument(
        "--index-filenames",
        help="the filenames that the dev server probes to find an "
             "index page",
        default=",".join(DEFAULT_INDEX_FILENAMES),
    )
    serve_parser.add_argument(
        "-p", "--port",
        type=int,
        default=8080,
        help="the port to listen to",
    )

    subparsers.add_parser(
        "version",
        help="outputs the version of thoughtwrapper you're currently "
             "running",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    args = arg_parser.parse_args()

    if args.command == "version":
        print(__version__)  # noqa: T201
        sys.exit(0)

    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=loglevel)

    match args.command:
        case "build":
            if args.output is None and args.single is None:
                args.output = Path.cwd().joinpath("target")

            if args.single is None:
                site.build(args.output)
            else:
                with _open_output(args.output) as output:
                    site.build_single(args.single, output)
        case "serve":
            server = DevServer(
                site,
                (args.host, args.port),
                index_filenames=args.index_filenames.split(","),
            )
            print(  # noqa: T201
                f"Starting server at http://{args.host}:{args.port}",
            )
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("Closing server")  # noqa: T201
        case _:
            raise RuntimeError(
                f"encountered unknown command: {args.command}",
            )

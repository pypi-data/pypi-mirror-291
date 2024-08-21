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

import io
import os
from pathlib import Path

import pytest
import thoughtwrapper

from .site import pipeline, pipeline_mixed_loader, site

dirpath = Path(__file__).parent.resolve()

routes = [
    {
        "path": "autoescape.html",
        "sourcepath": dirpath.joinpath("templates/autoescape.jinja"),
        "content": b"This checks if &lt;b&gt;auto-escaping&lt;/b&gt; is "
                   b"enabled.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("templates/autoescape.jinja"),
        ),
    },
    {
        "path": "basic.txt",
        "sourcepath": dirpath.joinpath("templates/basic.jinja"),
        "content": b"This is a very simple template in the Jinja templating "
                   b"language.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("templates/basic.jinja"),
        ),
    },
    {
        "path": "include.txt",
        "sourcepath": dirpath.joinpath("templates/include.jinja"),
        "content": b"Including: This is a very simple template in the Jinja "
                   b"templating language. End.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("templates/include.jinja"),
            dirpath.joinpath("templates/basic.jinja"),
        ),
    },
    {
        "path": "include_indirect.txt",
        "sourcepath": dirpath.joinpath("templates/include_indirect.jinja"),
        "content": b"Indirect: Including: This is a very simple template in "
                   b"the Jinja templating language. End. End indirect.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("templates/include_indirect.jinja"),
            dirpath.joinpath("templates/include.jinja"),
            dirpath.joinpath("templates/basic.jinja"),
        ),
    },
    {
        "path": "layout.txt",
        "sourcepath": dirpath.joinpath("templates/layout_child.jinja"),
        "content": b"This is a layout. Content from layout child. End.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("templates/layout_child.jinja"),
            dirpath.joinpath("templates/layout_parent.jinja"),
        ),
    },
    {
        "path": "metadata.txt",
        "sourcepath": dirpath.joinpath("templates/metadata.jinja"),
        "content": b"The value of foo is: bar",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("templates/metadata.jinja"),
        ),
    },
    {
        "path": "mixed-loader.txt",
        "sourcepath": dirpath.joinpath("templates/include_indirect.jinja"),
        "content": b"Indirect: Mixed layout: This is a very simple template "
                   b"in the Jinja templating language. End indirect.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("templates/include_indirect.jinja"),
            dirpath.joinpath("templates/basic.jinja"),
            dynamic=True,
        ),
    },
    {
        "path": "no-autoescape.html",
        "sourcepath": dirpath.joinpath("templates/autoescape.jinja"),
        "content": b"This checks if <b>auto-escaping</b> is enabled.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("templates/autoescape.jinja"),
        ),
    },
    {
        "path": "wrap-all-defaults.txt",
        "sourcepath": dirpath.joinpath("wrap-all-defaults.txt"),
        "content":
            b"This is a layout. Wrapped content.\n Some other placeholder. "
            b"End.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("wrap-all-defaults.txt"),
            dirpath.joinpath("templates/wrap_layout.jinja"),
        ),
    },
    {
        "path": "wrap-block-override.txt",
        "sourcepath": dirpath.joinpath("wrap-block-override.txt"),
        "content": b"This is a layout. A placeholder. Wrapped content.\n End.",
        "dependencies": thoughtwrapper.Dependencies(
            dirpath.joinpath("wrap-block-override.txt"),
            dirpath.joinpath("templates/wrap_layout.jinja"),
        ),
    },
    {
        "path": "wrap-key-overrides.txt",
        "content": b"This is a layout. A placeholder. Wrapped content.\n End.",
    },

    # note that Jinja trims the trailing line break by default.
    {
        "path": "wrap-passthrough.txt",
        "content": b"Wrapped content.",
    },
    {
        "path": "wrap-disabled.txt",
        "content": b"Wrapped content.",
    },
]


@pytest.mark.parametrize("route", routes)
def test_build(route):
    os.chdir(dirpath)

    with io.BytesIO() as f:
        site.build_single(route["path"], f)
        content = f.getvalue()

    assert content == route["content"]


@pytest.mark.parametrize("route", [x for x in routes if "sourcepath" in x])
def test_dependencies(route):
    route_pipeline = (
        pipeline_mixed_loader if route["path"] == "mixed-loader.txt"
        else pipeline
    )

    source = thoughtwrapper.FileSource(route["sourcepath"])
    _, dependencies = route_pipeline.run(source)

    expected_deps = (
        route["dependencies"] if "dependencies" in route
        else thoughtwrapper.Dependencies()
    )

    assert dependencies == expected_deps

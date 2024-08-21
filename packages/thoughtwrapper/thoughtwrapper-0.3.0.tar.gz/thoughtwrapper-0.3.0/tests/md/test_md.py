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

from .site import site

dirpath = Path(__file__).parent.resolve()

with dirpath.joinpath("hello-expected.html").open("rb") as f:
    hello_expected = f.read()
with dirpath.joinpath("syntax-expected.html").open("rb") as f:
    syntax_expected = f.read()

routes = [
    {
        "path": "hello.html",
        "content": hello_expected,
    },
    {
        "path": "syntax.html",
        "content": syntax_expected,
    },
]


@pytest.mark.parametrize("route", routes)
def test_build(route):
    os.chdir(dirpath)

    with io.BytesIO() as f:
        site.build_single(route["path"], f)
        content = f.getvalue()

    assert content == route["content"]

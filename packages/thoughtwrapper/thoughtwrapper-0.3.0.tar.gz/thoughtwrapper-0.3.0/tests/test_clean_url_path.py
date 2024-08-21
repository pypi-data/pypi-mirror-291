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

import pytest
import thoughtwrapper

valid_testdata = [
    {
        "expected": "foo",
        "url_paths": [
            "foo", "/foo", "//foo", "foo/", "foo//", "/foo/", "//foo/",
            "//foo//", "/foo//", "foo/.", "foo/../foo", "foo/bar/..",
            "/foo/bar/../",
        ],
    },
    {
        "expected": "foo/bar",
        "url_paths": [
            "foo/bar", "foo/bar/baz/..", "foo/./bar", "foo/./../foo/bar",
            "foo/bar/baz/../../bar", "baz/../foo/bar",
        ],
    },
]

invalid_url_paths = [
    "", "/", "//", "///", ".", "./", "./.", "././.", "/./", "/./.", "//././/",
    "..", "foo/..", "foo/../..", "foo/bar/../..",
]

@pytest.mark.parametrize("testdata", valid_testdata)
def test_clean_url_path_happy(testdata):
    for url_path in testdata["url_paths"]:
        actual = thoughtwrapper.clean_url_path(url_path)
        assert actual == testdata["expected"]

@pytest.mark.parametrize("url_path", invalid_url_paths)
def test_clean_url_path_invalid(url_path):
    with pytest.raises(thoughtwrapper.InvalidPathError):
        thoughtwrapper.clean_url_path(url_path)

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

from pathlib import PurePath

import thoughtwrapper
from thoughtwrapper import BytesSource, Dependencies, StringSource

site = thoughtwrapper.Site()
pipeline = thoughtwrapper.Pipeline()

site.add_route(pipeline, "test1.html", "test1.html")
site.add_route(pipeline, "foo/test2/index.html", "test2.html")

site.add_routes(pipeline, {
    "bar/test3.txt": "test3.txt",
    "images/test4.jpg": "test4.jpg",
})

site.add_route(
    pipeline, "test5.txt",
    BytesSource(b"This is a raw bytes route!", Dependencies()),
)
site.add_route(
    pipeline, "test6.txt",
    StringSource("This is a string route!", Dependencies()),
)

site.add_route(
    pipeline, PurePath("test7.txt"),
    StringSource("This is a path-like route!", Dependencies()),
)

thoughtwrapper.run(site)

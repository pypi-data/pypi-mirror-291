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

import jinja2
import thoughtwrapper
from thoughtwrapper.extras import frontmatter, template

site = thoughtwrapper.Site()

pipeline = thoughtwrapper.Pipeline()
pipeline.add_filter(frontmatter.Loader())
pipeline.add_filter(template.Engine(
    {
        "loader": jinja2.FileSystemLoader("templates"),
    },
    layout_wrapper_enabled=True,
))
site.add_routes(pipeline, {
    "basic.txt": "templates/basic.jinja",
    "include.txt": "templates/include.jinja",
    "include_indirect.txt": "templates/include_indirect.jinja",
    "layout.txt": "templates/layout_child.jinja",
})

if __name__ == "__main__":
    thoughtwrapper.run(site)

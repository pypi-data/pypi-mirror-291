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
from thoughtwrapper.extras import frontmatter, metadata, template

site = thoughtwrapper.Site()

pipeline = thoughtwrapper.Pipeline()
pipeline.add_filter(frontmatter.Loader())
pipeline.add_filter(template.Engine({
    "loader": jinja2.FileSystemLoader("."),
    "autoescape": False,
}))

merge_pipeline = thoughtwrapper.Pipeline()
merge_pipeline.add_filter(metadata.Injector({
    "foo": "hello",
    "bar": {
        "baz": "this will be replaced",
        "extra": "this too",
    },
}, thoughtwrapper.Dependencies()))
merge_pipeline.add_filter(frontmatter.Loader())
merge_pipeline.add_filter(template.Engine({
    "loader": jinja2.FileSystemLoader("."),
    "autoescape": False,
}))

plus_pipeline = thoughtwrapper.Pipeline()
plus_pipeline.add_filter(frontmatter.Loader(
    separator_line="+++",
))
plus_pipeline.add_filter(template.Engine({
    "loader": jinja2.FileSystemLoader("."),
    "autoescape": False,
}))

site.add_routes(pipeline, {
    "dash.txt": "dash.jinja",

    "empty.txt": "empty.jinja",
    "multi.txt": "multi.jinja",
    "passthrough.txt": "passthrough.jinja",
})
site.add_route(merge_pipeline, "merge.txt", "merge.jinja")
site.add_route(plus_pipeline, "plus.txt", "plus.jinja")

if __name__ == "__main__":
    thoughtwrapper.run(site)

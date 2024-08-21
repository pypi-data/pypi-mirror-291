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
    "autoescape.html": "templates/autoescape.jinja",
    "basic.txt": "templates/basic.jinja",
    "include.txt": "templates/include.jinja",
    "include_indirect.txt": "templates/include_indirect.jinja",
    "layout.txt": "templates/layout_child.jinja",
    "metadata.txt": "templates/metadata.jinja",
    "wrap-all-defaults.txt": "wrap-all-defaults.txt",
    "wrap-block-override.txt": "wrap-block-override.txt",
})

pipeline_key_overrides = thoughtwrapper.Pipeline()
pipeline_key_overrides.add_filter(frontmatter.Loader())
pipeline_key_overrides.add_filter(template.Engine(
        {
            "loader": jinja2.FileSystemLoader("templates"),
        },
        layout_wrapper_enabled=True,
        lw_tpl_key=["foo", "bar", "lyt"],
        lw_block_key=["foo", "bar", "blk"],
))
site.add_routes(pipeline_key_overrides, {
    "wrap-key-overrides.txt": "wrap-key-overrides.txt",
    "wrap-passthrough.txt": "wrap-all-defaults.txt",
})

pipeline_wrap_disabled = thoughtwrapper.Pipeline()
pipeline_wrap_disabled.add_filter(frontmatter.Loader())
pipeline_wrap_disabled.add_filter(template.Engine({
    "loader": jinja2.FileSystemLoader("templates"),
}))
site.add_route(
    pipeline_wrap_disabled,
    "wrap-disabled.txt", "wrap-all-defaults.txt",
)

pipeline_no_autoescape = thoughtwrapper.Pipeline()
pipeline_no_autoescape.add_filter(template.Engine({
    "loader": jinja2.FileSystemLoader("templates"),
    "autoescape": False,
}))
site.add_route(
    pipeline_no_autoescape,
    "no-autoescape.html", "templates/autoescape.jinja",
)

class MixedLoader(jinja2.BaseLoader):
    def __init__(self):
        self.__wrapped = jinja2.FileSystemLoader("templates")

    def get_source(self, environment, template):
        if template == "basic.jinja":
            return self.__wrapped.get_source(environment, template)
        if template == "include.jinja":
            return [
                'Mixed layout: {% include "basic.jinja" %}',
                None,
                None,
            ]

        raise RuntimeError(
            f"requested unknown template from MixedLoader: {template}",
        )

pipeline_mixed_loader = thoughtwrapper.Pipeline()
pipeline_mixed_loader.add_filter(template.Engine({
    "loader": MixedLoader(),
}))
site.add_route(
    pipeline_mixed_loader,
    "mixed-loader.txt", "templates/include_indirect.jinja",
)

if __name__ == "__main__":
    thoughtwrapper.run(site)

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

import thoughtwrapper
from thoughtwrapper.extras import md, syntax

site = thoughtwrapper.Site()

pipeline = thoughtwrapper.Pipeline()
pipeline.add_filter(md.Renderer())

syn_pipeline = thoughtwrapper.Pipeline()
syn_pipeline.add_filter(md.Renderer())
syn_pipeline.add_filter(syntax.Highlighter())

site.add_route(pipeline, "hello.html", "hello.md")
site.add_route(syn_pipeline, "syntax.html", "hello.md")

if __name__ == "__main__":
    thoughtwrapper.run(site)

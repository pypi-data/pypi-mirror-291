<!--
For the avoidance of doubt, the information in this comment block applies to
this README file only.

Copyright (C) 2024 Lucas Hinderberger
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# ![thoughtwrapper - A Static Site Generator for Tinkerers](logo/logo-light.svg)

## Summary
It is designed around the idea of **maximum flexibility** while still remaining
**simple and easy to understand**. Unlike most other static site generators,
thoughtwrapper **does not enforce a particular layout or paradigm** (e.g. blog)
on your site's sources or contents. It is a very liberal framework, in which
you can **compose your own build pipeline(s)** using **simple, transparent,
chainable filters**. Nearly every aspect of the build is **customizable and
scriptable**.

This is what a thoughtwrapper build script looks like:

```python
from pathlib import Path

import thoughtwrapper
from thoughtwrapper.extras import md, syntax

site = thoughtwrapper.Site()

pipeline = thoughtwrapper.Pipeline()
pipeline.add_filter(md.Renderer())
pipeline.add_filter(syntax.Highlighter())

static_pipeline = thoughtwrapper.Pipeline()

site.add_routes(pipeline, {
    p.relative_to("pages").with_suffix(".html"): p
    for p in Path().glob("pages/**/*.md")
})

site.add_routes(static_pipeline, {
    p: p for p in Path().glob("static/**/*")
})

thoughtwrapper.run(site)
```

Read more about thoughtwrapper on <https://thoughtwrapper.libretastic.org>.


## Installation
thoughtwrapper can be installed using the following methods:

### Pre-Packaged
thoughtwrapper is available from the following package repositories:

#### From PyPI
thoughtwrapper is available on PyPI at
<https://pypi.org/project/thoughtwrapper>

When using pip, you can add it to your project using:

```bash
pip install thoughtwrapper[md,syntax,template]
```

Installation on other project / package managers is similar. Refer to the
manual of your tool of choice for details.

#### From Release Wheels
Release wheels are also published to Codeberg at
<https://codeberg.org/lhinderberger/thoughtwrapper/releases>

### Build From Source
To build thoughtwrapper from its source code, follow the instructions below:

#### Prerequisites
Before you can build thoughtwrapper from source, there is a number of
prerequisites that need to be met.

You need to have the following software installed on your system:

- Python v3.12 or higher
- PDM v2.17 or higher

#### Building the Project
A release build of the project into the Wheel format (and also into sdist) is
performed by running:

```bash
pdm install -G :all
pdm build
```

#### Running Tests
You can run the tests for thoughtwrapper by calling:

```
pdm run pytest
```

#### Viewing documentation offline
The documentation for thoughtwrapper can be viewed from its source tree (if
you have installed it correctly as described in "building from source") by
running

```bash
pdm run docpreview
```


## Usage
Usage is described on thoughtwrapper's website at
<https://thoughtwrapper.libretastic.org>

Documentation is also available in the `doc` subdirectory.


## Issues
Have you encountered a bug or do you want to request improvements?

Please check whether the issue in question has already been added to the issue
tracker. If not, feel free to create a new issue.

**If you have found a security issue, do not open an issue on the issue
tracker! Instead, write an email to the maintainer (the contact data can be
found at the end of this README)**

You can find the issue tracker for thoughtwrapper at:
<https://codeberg.org/lhinderberger/thoughtwrapper/issues>

When participating in the thoughtwrapper issue tracker, please respect the code
of conduct, which can be found at [CONDUCT.md](./CONDUCT.md)


## Versioning and Compatibility
thoughtwrapper follows Semantic Versioning, as described at
<https://semver.org/spec/v2.0.0.html>
in the subset that is compatible to Python's Version Specifies, as described at
<https://packaging.python.org/en/latest/specifications/version-specifiers/>

Note that the package version is only bumped on release (meaning on tagged
releases).

thoughtwrapper targets Python v3.12 or later.


## License
<!-- REUSE-IgnoreStart -->
```
thoughtwrapper - A Static Site Generator for Tinkerers
Copyright (C) 2024 The thoughtwrapper Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
<!-- REUSE-IgnoreEnd -->

Please refer to [LICENSE.txt](./LICENSE.txt) for details.


## Contributing
Contributions to thoughtwrapper are welcome!

Please refer to [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

This project does not accept financial contributions / donations and it does
not offer any professional services.


## Maintainer and Contact
At the time of writing, thoughtwrapper is maintained by
Lucas Hinderberger (mail@lucas-hinderberger.de).

GPG public keys are available at:
<https://lucas-hinderberger.de/gpg>

Additional contact information is available at:
<https://lucas-hinderberger.de/imprint>

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

import os
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO


@contextmanager
def open_output(path: str | os.PathLike | None) -> BinaryIO:
    """Return a contextmanager over the output file as specified via CLI.

    :param path: The path to the output file. If None, stdout will be
        used and the contextmanager will not attempt to close it.
    """
    if path is None:
        yield sys.stdout.buffer
        return

    path = Path(path)

    f = None
    try:
        dirpath = path.parent
        dirpath.mkdir(parents=True, exist_ok=True)
        f = path.open("wb")
    except Exception as e:
        raise RuntimeError(f'Could not open output file at "{path}"') from e

    yield f

    f.close()

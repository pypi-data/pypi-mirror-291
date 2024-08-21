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

import http.client
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

dirpath = Path(__file__).parent


# This test is supposed to detect regressions in cache invalidation.
# The strategy is to launch a dev server, render routes, check the output, then
# change the input while the dev server is still running and check if the
# output has changed accordingly.


def request_and_check(conn, path, expected_content):
    conn.request("GET", "/" + path)
    response = conn.getresponse()

    print("Response retrieved")

    content = response.read()
    content_len = response.getheader("Content-Length")
    if content_len is not None:
        content_len = int(content_len)

    assert response.status == 200
    assert content_len == len(expected_content)
    assert content == expected_content


def test_cache(tmp_path):
    host = "localhost"
    port = 8099

    sitepath = tmp_path.joinpath("site")
    shutil.copytree(dirpath.joinpath("site"), sitepath)

    with subprocess.Popen(
        [
            sys.executable,
            "site.py",
            "-v",
            "serve",
            "--host", host,
            "-p", str(port),
        ],
        cwd=sitepath,
    ) as proc:
        print("Server subprocess is running")

        try:
            # Wait until port is available, or proc is cancelled, or timeout
            print("Waiting for open port")
            for i in range(10):
                if proc.poll() is not None:
                    raise RuntimeError("could not start server")
                print(f"Attempt {i+1}/10")
                try:
                    with socket.create_connection((host, port), timeout=1):
                        break
                except ConnectionRefusedError:
                    time.sleep(1)

            print("Port is open")

            conn = http.client.HTTPConnection(host, port, timeout=10)
            try:
                request_and_check(
                    conn, "basic.txt",
                    b"This is a very simple template in "
                    b"the Jinja templating language.",
                )
                request_and_check(
                    conn, "include.txt",
                    b"Including: This is a very simple template in "
                    b"the Jinja templating language. End.",
                )
                request_and_check(
                    conn, "include_indirect.txt",
                    b"Indirect: Including: This is a very simple template in "
                    b"the Jinja templating language. End. End indirect.",
                )
                request_and_check(
                    conn, "layout.txt",
                    b"This is a layout. Content from layout child. End.",
                )

                with (
                    sitepath.joinpath("templates/layout_parent.jinja")
                            .open("w")
                ) as f:
                    f.write(
                        "Modified layout with "
                        "{% block content %}Placeholder{% endblock %}",
                    )
                request_and_check(
                    conn, "layout.txt",
                    b"Modified layout with Content from layout child.",
                )

                with (
                    sitepath.joinpath("templates/include_indirect.jinja")
                            .open("w")
                ) as f:
                    f.write('Modified indirect: {% include "include.jinja" %}')
                request_and_check(
                    conn, "include_indirect.txt",
                    b"Modified indirect: Including: This is a very simple "
                    b"template in the Jinja templating language. End.",
                )

                with (
                    sitepath.joinpath("templates/include.jinja")
                            .open("w")
                ) as f:
                    f.write('Modified include: {% include "basic.jinja" %}')
                request_and_check(
                    conn, "include_indirect.txt",
                    b"Modified indirect: Modified include: This is a very "
                    b"simple template in the Jinja templating language.",
                )
                request_and_check(
                    conn, "include.txt",
                    b"Modified include: This is a very simple template in "
                    b"the Jinja templating language.",
                )

                with (
                    sitepath.joinpath("templates/basic.jinja")
                            .open("w")
                ) as f:
                    f.write("Modified basic")
                request_and_check(
                    conn, "include_indirect.txt",
                    b"Modified indirect: Modified include: Modified basic",
                )
                request_and_check(
                    conn, "include.txt",
                    b"Modified include: Modified basic",
                )
                request_and_check(
                    conn, "basic.txt",
                    b"Modified basic",
                )
            finally:
                print("Closing connection")
                conn.close()
        finally:
            print("Sending SIGNINT to server")
            proc.send_signal(signal.SIGINT)

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
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

dirpath = Path(__file__).parent

routes = [
    {
        "path": "test1.html",
        "path_alias": [
            "test1.html?foo",
            "test1.html?foo=bar",
            "test1.html?foo=bar&bar=baz",
        ],
        "content": dirpath.joinpath("test1.html").read_bytes(),
        "contentType": "text/html",
    },
    {
        "path": "foo/test2/index.html",
        "path_alias": [
            "foo/test2", "foo/test2/",
            "foo/test2/index.html?bar", "foo/test2?bar", "foo/test2/?bar",
            "foo/test2?bar=baz", "foo/test2?foo=bar&bar=baz",
        ],
        "content": dirpath.joinpath("test2.html").read_bytes(),
        "contentType": "text/html",
    },
    {
        "path": "bar/test3.txt",
        "content": dirpath.joinpath("test3.txt").read_bytes(),
        "contentType": "text/plain",
    },
    {
        "path": "images/test4.jpg",
        "content": dirpath.joinpath("test4.jpg").read_bytes(),
        "contentType": "image/jpeg",
    },
    {
        "path": "test5.txt",
        "content": b"This is a raw bytes route!",
        "contentType": "text/plain",
    },
    {
        "path": "test6.txt",
        "content": b"This is a string route!",
        "contentType": "text/plain",
    },
    {
        "path": "test7.txt",
        "content": b"This is a path-like route!",
        "contentType": "text/plain",
    },
]


@pytest.mark.parametrize("route", routes)
def test_build_to_stdout(route):
    result = subprocess.run(  # noqa: PLW1510
        [
            sys.executable,
            "site.py",
            "build",
            "-s", route["path"],
        ],
        capture_output=True,
        cwd=dirpath,
    )

    assert result.returncode == 0
    assert result.stdout == route["content"]


@pytest.mark.parametrize("route", routes)
def test_build_to_file(tmp_path, route):
    outpath = tmp_path.joinpath("out.bin")

    result = subprocess.run(  # noqa: PLW1510
        [
            sys.executable,
            "site.py",
            "build",
            "-s", route["path"],
            "-o", outpath,
        ],
        capture_output=True,
        cwd=dirpath,
    )
    assert result.returncode == 0

    actual_content = outpath.read_bytes()
    assert actual_content == route["content"]


def test_build_to_dir(tmp_path):
    result = subprocess.run(  # noqa: PLW1510
        [
            sys.executable,
            "site.py",
            "build",
            "-o", tmp_path,
        ],
        cwd=dirpath,
    )
    assert result.returncode == 0

    for route in routes:
        outpath = tmp_path.joinpath(route["path"])

        actual_content = outpath.read_bytes()
        assert actual_content == route["content"]


@pytest.fixture(scope="module")
def devserver_conn():
    host = "localhost"
    port = 8099

    with subprocess.Popen(
        [
            sys.executable,
            "site.py",
            "serve",
            "--host", host,
            "-p", str(port),
        ],
        cwd=dirpath,
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
                yield conn
            finally:
                print("Closing connection")
                conn.close()
        finally:
            print("Sending SIGNINT to server")
            proc.send_signal(signal.SIGINT)


@pytest.mark.parametrize("route", routes)
def test_serve(devserver_conn, route):
    all_paths = [route["path"]]
    if "path_alias" in route:
        all_paths += route["path_alias"]

    for path in all_paths:
        devserver_conn.request("GET", "/" + path)
        response = devserver_conn.getresponse()

        print("Response retrieved")

        content = response.read()
        content_len = response.getheader("Content-Length")
        if content_len is not None:
            content_len = int(content_len)
        content_type = response.getheader("Content-Type")

        assert response.status == 200
        assert content_len == len(route["content"])
        assert content_type == route["contentType"]
        assert content == route["content"]

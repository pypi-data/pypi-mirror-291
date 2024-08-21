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

"""Template rendering support using the Jinja2 library."""

import logging
import threading
from collections.abc import Callable
from copy import deepcopy
from typing import Any, override

import jinja2

from thoughtwrapper import Dependencies, Filter, Stage

__all__ = ["Engine"]


class Engine(Filter):
    """A thoughtwrapper Filter for rendering templates.

    This filter uses the Jinja2 library as its rendering engine. The
    Environment class is exposed to ensure maximum configurability.

    In addition to simple template rendering directly where raw input is
    treated as a template, this Filter optionally supports wrapping
    non-template input with a layout template. If the layout wrapper is
    enabled, input can declare that it wants to be rendered inside a
    layout by configuring the layout's name in its metadata dictionary.
    The raw input will then be rendered as the contents of a
    configurable block within the layout.
    """

    def __init__(  # noqa: PLR0913
        self, env_params: dict,
                 layout_wrapper_enabled: bool = False,  # noqa: FBT001, FBT002
        lw_tpl_key: str | list[str] = "layout",
        lw_block_key: str | list[str] = "layout_block",
        lw_block_default: str = "content",
        input_encoding: str = "UTF-8",
        output_encoding: str = "UTF-8",
    ):
        """Create a new template engine Filter.

        The arguments (except for env_params) will be used to initialize
        instance properties of the same name.

        The jinja2.Environment will be stored in an instance property of
        name environment.

        :param env_params: Parameters that are passed on to the
            constructor for jinja2.Environment.
        :param layout_wrapper_enabled: Enables or disables the layout
            wrapper feature (see :class:`Engine`).
        :param lw_tpl_key: This is the metadata key under which the
            layout template name shall be looked up. If this is a list
            and metadata is composed of nested dictionaries, the
            elements of this list form a path through the metadata.
        :param lw_block_key: This is the metadata key under
            which the layout block name (that is the name of the layout
            block that content shall be rendered to) shall be looked up.
            If this is a list and metadata is composed of nested
            dictionaries, the elements of this list form a path through
            the metadata.
        :param lw_block_default: The name of the layout block that
            content shall be rendered to, if no block is specified
            explicitly through lw_block_key.
        :param input_encoding: The encoding that is used for template
            sources (raw bytes input).
        :param output_encoding: The encoding that will be used for
            coverting the template output to bytes.

        Note that, for security reasons, unless an "autoescape" key is
        explicitly set in env_params, "autoescape" will be set to True.
        This may differ from Jinja2's default setting.

        Warning: If a loader is specified, this function will mutate it
        by wrapping its get_source method (for dependency detection
        purposes). Also, up_to_date callbacks returned by get_source
        will be wrapped.
        """
        if lw_tpl_key is None:
            lw_tpl_key = ["frontmatter", "layout"]
        if lw_block_key is None:
            lw_block_key = ["frontmatter", "layout_block"]

        self._dependencies = Dependencies()
        self._deps_lock = threading.Lock()

        self.layout_wrapper_enabled = layout_wrapper_enabled
        self.lw_tpl_key = lw_tpl_key
        self.lw_block_key = lw_block_key
        self.lw_block_default = lw_block_default

        self.input_encoding = input_encoding
        self.output_encoding = output_encoding

        if "autoescape" not in env_params:
            env_params["autoescape"] = True

        if "loader" in env_params:
            env_params = env_params.copy()
            _wrap_loader(env_params["loader"], self._dependencies)

        # The S701 lint is disabled because autoescape is added further above,
        # unless the user has explicitly set it previously.
        self.environment = jinja2.Environment(**env_params)  # noqa: S701

    @override
    def stages(self) -> list[Stage]:
        """Override stages method of Filter."""
        return [Stage.RAW]

    @override
    def filter_raw(
        self, raw: bytes, metadata: dict,
    ) -> tuple[bytes, Dependencies]:
        """Override filter_raw method of Filter."""
        with self._deps_lock:
            self._dependencies.clear()

            decoded_raw = raw.decode(self.input_encoding)

            wrap_layout, wrap_block = self.extract_wrap_params(metadata)

            if self.layout_wrapper_enabled and wrap_layout is not None:
                logging.debug(
                    'wrapping content into layout "%s", block "%s"',
                    wrap_layout, wrap_block,
                )

                metadata["_tw"]["wrapped"] = decoded_raw
                template_src = self.compile_wrap_template(
                    wrap_layout,
                    wrap_block,
                )
            else:
                logging.debug("rendering regular template")
                template_src = decoded_raw

            template = self.environment.from_string(template_src)
            out = template.render(metadata)

            return (
                bytes(out, self.output_encoding),
                deepcopy(self._dependencies),
            )

    def compile_wrap_template(self, layout: str, block: str) -> str:
        """Compile instructions for Jinja for wrapping content in a template.

        The output of this function is a trivial template that can be
        passed to the Jinja templating engine for the purpose of gluing
        together user-provided content and user-provided layout. The
        compilation result contains only control statements, no content.

        User-provided raw content can be inserted into the template
        returned from this function using the template parameter
        specified in :py:attr:`raw_key`.
        """
        if not block.isidentifier():
            raise RuntimeError(
                "block name for layout wrapping must be a valid identifier",
            )

        layout = layout.replace("\\", "\\\\").replace('"', '\\"')

        instructions = '{% extends "' + layout + '" %}'
        instructions += "{% block " + block + " %}"
        instructions += "{{ _tw.wrapped | safe }}"
        instructions += "{% endblock %}"

        return instructions

    def extract_wrap_params(  # noqa: C901
        self, metadata: dict,
    ) -> tuple[str, str]:
        """Extract the parameters for layout wrapping from metadata.

        Returns a tuple of layout name and block name, as defined in the
        given metadata object under the keys configured in
        :py:attr:`lw_tpl_key` and
        :py:attr:`lw_block_key`.

        If no layout name is specified, a tuple of None and block name
        is returned.

        If no block name is specified, it will be replaced by
        :py:attr:`lw_block_default`.
        """
        def lookup(d: dict, keys: str | list[str]) -> Any:
            if isinstance(keys, str):
                keys = [keys]
            for k in keys:
                d = d.get(k)
                if d is None:
                    return None
            return d

        layout = None
        v = lookup(metadata, self.lw_tpl_key)
        if v is not None:
            if not isinstance(v, str):
                raise RuntimeError("wrap layout name must be of type string")
            if v == "":
                raise RuntimeError("wrap layout name must not be empty")

            layout = v

        block = self.lw_block_default
        v = lookup(metadata, self.lw_block_key)
        if v is not None:
            if not isinstance(v, str):
                raise RuntimeError("wrap layout block must be of type string")
            if v == "":
                raise RuntimeError("wrap layout block must not be empty")

            block = v

        return (layout, block)


def _wrap_loader(loader: jinja2.BaseLoader, dependencies: Dependencies):
    """Wrap a loader for dependency detection."""
    inner_get_source = loader.get_source

    def wrapper(
        environment: jinja2.Environment, template: str,
    ) -> tuple[str, str|None, Callable[[None],bool]]:
        source, filename, up_to_date = inner_get_source(environment, template)

        tpl_dependencies = (
            Dependencies(dynamic=True) if filename is None
            else Dependencies(filename)
        )

        dependencies.update(tpl_dependencies)

        def up_to_date_wrapper() -> bool:
            dependencies.update(tpl_dependencies)

            if up_to_date is None:
                # At the time of writing, Jinja2 assumes that a source
                # is up-to-date if up_to_date is None (see Jinja2 v3.1.4
                # src/jinja2/environment.py, L. 1495 ff.)
                return True

            return up_to_date()

        return (source, filename, up_to_date_wrapper)

    loader.get_source = wrapper

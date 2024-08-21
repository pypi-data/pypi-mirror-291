"""
## This module defines a base class for jinja2 extensions that generate images.
"""

import enum
import inspect
import json
import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any, cast
from uuid import UUID, uuid5

import yaml
from jinja2 import Environment, nodes, pass_context
from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2.runtime import Context, Macro

logger = logging.getLogger(__name__)

namespace = UUID("b5db653c-cc06-466c-9b39-775db782a06f")


class Mode(enum.Enum):
    MD: str = "md"
    OUT: str = "out"
    RST: str = "rst"
    MYST: str = "myst"


LOOKUP_MODE = {
    "md": Mode.MD,
    "markdown": Mode.MD,
    "out": Mode.OUT,
    "output": Mode.OUT,
    "output_only": Mode.OUT,
    "output_path": Mode.OUT,
    "rst": Mode.RST,
    "restructuredtext": Mode.RST,
    "myst": Mode.MYST,
    "myst_parser": Mode.MYST,
    "myst_markdown": Mode.MYST,
}


class GenImageExtension(Extension):
    tags: set[str] = {"yaml"}  # noqa: RUF012
    output_root_key: str | None = None

    def __init__(self, environment: Environment):
        super().__init__(environment)

    def parse(self, parser: Parser) -> nodes.Node:
        """
        The logic to parse the jinja2 block as yaml.
        """
        line = next(parser.stream).lineno
        block = parser.parse_statements((f"name:end{next(iter(self.tags))}",), drop_needle=True)
        kwargs = yaml.safe_load(cast(nodes.TemplateData, cast(nodes.Output, block[0]).nodes[0]).data)
        callback = self.call_method("_render", [nodes.Const(json.dumps(kwargs))])
        return nodes.CallBlock(callback, [], [], block).set_lineno(line)

    @staticmethod
    def modify(**kwargs: Any) -> Generator[tuple[str, Any], None, None]:
        """
        Intercept and modify the keyword arguments before passing them to the callback function.
        """
        yield from kwargs.items()

    def callback(self, inp: Path | str, out: Path, **kwargs: Any) -> None:
        """
        The function to call to generate an image.
        """
        raise NotImplementedError

    @property
    def _valid_keys(self) -> Generator[str]:
        yield from ()

    @pass_context
    def _render(self, context: Context, kwargs_json: str, caller: Macro) -> str:
        kwargs = dict(self.modify(**json.loads(kwargs_json)))
        valid_keys = set(inspect.signature(self._gen_markdown_lines).parameters) | set(self._valid_keys)
        valid_keys = valid_keys - {"context", "output_name_salt", "out"}
        unknown_keys = set(kwargs.keys()) - valid_keys
        if any(unknown_keys):
            raise TypeError(f"callback got unexpected keyword arguments: {', '.join(unknown_keys)}")

        return "\n".join(self._gen_markdown_lines(context, output_name_salt=kwargs_json, **kwargs))

    def _gen_markdown_lines(
        self,
        context: Context,
        inp: Path | str,
        ext: str = ".png",
        name: str | None = None,
        mode: str | Mode = Mode.OUT,
        align: str = "center",
        caption: str | None = None,
        use_cached: bool = True,
        output_name_salt: str = "...",
        **kwargs: Any,
    ) -> Generator[str, None, None]:
        """
        Run callback and yield a series of markdown commands to include it .
        """
        if isinstance(mode, str):
            mode = LOOKUP_MODE[mode.strip().lower()]

        root = self._get_output_root(context)
        if name is None:
            name = str(uuid5(namespace, str(inp) + output_name_salt))

        out = root.joinpath(name).with_suffix("." + ext.lower().lstrip("."))

        if not out.exists() or not use_cached:
            self.callback(inp=inp, out=out, **kwargs)
        else:
            logger.warning("existing: %s", out)

        if mode == Mode.OUT:
            yield str(out)
        elif mode == Mode.MD:
            if caption is not None:
                yield f"![{caption}]({out.name})"
            else:
                yield f"![{out.name}]"
        elif mode == Mode.RST:
            if caption is not None:
                yield f".. image:: {out.name}\n   :alt: {caption}"
            else:
                yield f".. image:: {out.name}"
        elif mode == Mode.MYST:
            yield from self._render_myst(out, align, caption, kwargs)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    @classmethod
    def _get_output_root(cls, context: Context) -> Path:
        if cls._get_output_root is None:
            return Path.cwd()

        if (root := context.parent.get(str(cls.output_root_key))) is None:
            return Path.cwd()

        return Path(cast(Path, root))

    @staticmethod
    def _render_myst(out: Path, align: str, caption: str | None, kwargs: dict[str, Any]) -> Generator[str, None, None]:
        if caption is not None:
            yield f":::{{figure}} {out.name}"
        else:
            yield f":::{{image}} {out.name}"
        if kwargs.get("width") is not None:
            yield f":width: {kwargs['width']}px"
        if kwargs.get("height") is not None:
            yield f":height: {kwargs['height']}px"
        if align is not None:
            yield f":align: {align}"
        if caption is not None:
            yield f":\n{caption}"
        yield r":::"

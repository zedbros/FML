"""
Helpers for the manual agent loop: build OpenAI/OpenRouter tool specs from
typed Python functions, and pretty-print chat messages on the console.
"""
import inspect
import re
from typing import get_type_hints, get_origin, get_args, is_typeddict


# ---- Pretty printing for the conversation ----

_RESET = "\033[0m"
_DIM = "\033[2m"
_BLUE = "\033[34m"
_YELLOW = "\033[33m"
_GREEN = "\033[32m"
_CYAN = "\033[36m"

_ROLE_COLORS = {
    "system": _DIM,
    "user": _BLUE,
    "assistant": _YELLOW,
    "tool": _GREEN,
}


def pretty_print_message(message: dict, max_chars: int = 300) -> str:
    """Return a one-line, colored representation of a chat message.

    Handles the four roles produced by the agent loop: `system`, `user`,
    `assistant` (with optional `tool_calls`), and `tool`. Content longer than
    `max_chars` is truncated so the conversation history stays scannable.
    """
    return _format_message(message, max_chars=max_chars)


def pretty_print_response(response: dict) -> str:
    """Return a colored representation of a fresh assistant response.

    Same format as `pretty_print_message` but without truncation, so you can
    fully see what the model just produced.
    """
    return _format_message(response, max_chars=None)


def _format_message(message: dict, max_chars: int | None) -> str:
    role = message.get("role", "?")
    color = _ROLE_COLORS.get(role, "")
    label = f"{color}{role:>9}{_RESET}"

    if role == "assistant":
        parts: list[str] = []
        content = message.get("content")
        if content:
            parts.append(_truncate(content, max_chars))
        for tc in message.get("tool_calls") or []:
            parts.append(f"→ {_format_tool_call(tc)}")
        body = " | ".join(parts) or "(empty)"
        return f"{label} {body}"

    if role == "tool":
        tc_id = _short_id(message.get("tool_call_id", ""))
        content = _truncate(message.get("content") or "", max_chars)
        return f"{label} {_DIM}(id={tc_id}){_RESET} {content}"

    return f"{label} {_truncate(message.get('content') or '', max_chars)}"


def _format_tool_call(tc: dict) -> str:
    name = tc.get("function", {}).get("name", "?")
    args = tc.get("function", {}).get("arguments", "")
    return f"{_CYAN}{name}{_RESET}({args})"


def _short_id(s: str, n: int = 12) -> str:
    return s if len(s) <= n else s[:n] + "…"


def _truncate(s: str, n: int | None) -> str:
    s = str(s).replace("\n", " ↵ ")
    if n is None or len(s) <= n:
        return s
    return s[:n] + f"{_DIM}… (+{len(s) - n} chars){_RESET}"


# ---- Tool schema generation ----

_PRIMITIVES = {int: "integer", str: "string", bool: "boolean", float: "number"}


def tool_schema(fn) -> dict:
    """Build an OpenAI/OpenRouter tool spec from a typed Python function.

    The function's docstring provides:
      - the tool description (text before the `Args:` section)
      - per-argument descriptions (parsed from the `Args:` section, Google-style)

    Supported parameter types: int, str, bool, float, list[T], TypedDict.
    """
    sig = inspect.signature(fn)
    hints = get_type_hints(fn)
    description, arg_descriptions = _parse_docstring(inspect.getdoc(fn) or "")

    properties = {}
    required = []
    for name, param in sig.parameters.items():
        if name not in hints:
            raise ValueError(f"Parameter {name!r} of {fn.__name__} has no type hint")
        properties[name] = _type_to_schema(hints[name], arg_descriptions.get(name))
        if param.default is inspect.Parameter.empty:
            required.append(name)

    return {
        "type": "function",
        "function": {
            "name": fn.__name__,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }


def _type_to_schema(tp, description: str | None = None) -> dict:
    schema: dict = {}
    origin = get_origin(tp)

    if tp in _PRIMITIVES:
        schema["type"] = _PRIMITIVES[tp]
    elif origin is list:
        (item_type,) = get_args(tp)
        schema["type"] = "array"
        schema["items"] = _type_to_schema(item_type)
    elif is_typeddict(tp):
        item_hints = get_type_hints(tp)
        schema["type"] = "object"
        schema["properties"] = {k: _type_to_schema(v) for k, v in item_hints.items()}
        schema["required"] = list(item_hints.keys())
    elif tp is dict:
        schema["type"] = "object"
    else:
        raise ValueError(f"Unsupported type for tool schema: {tp!r}")

    if description:
        schema["description"] = description
    return schema


_SECTION = re.compile(r"^\s*(Args|Arguments|Parameters|Returns|Raises|Example|Examples)\s*:\s*$")
_ARGS_SECTION = re.compile(r"^\s*(Args|Arguments|Parameters)\s*:\s*$")
_ARG_LINE = re.compile(r"^\s+(\w+)\s*(?:\([^)]*\))?\s*:\s*(.+)$")


def _parse_docstring(doc: str) -> tuple[str, dict[str, str]]:
    """Parse a Google-style docstring into (description, {arg_name: arg_desc})."""
    if not doc:
        return "", {}

    lines = doc.splitlines()
    desc_lines: list[str] = []
    i = 0
    while i < len(lines) and not _SECTION.match(lines[i]):
        desc_lines.append(lines[i])
        i += 1
    description = "\n".join(desc_lines).strip()

    arg_descriptions: dict[str, str] = {}
    while i < len(lines):
        if _ARGS_SECTION.match(lines[i]):
            i += 1
            while i < len(lines) and not _SECTION.match(lines[i]):
                m = _ARG_LINE.match(lines[i])
                if m:
                    arg_descriptions[m.group(1)] = m.group(2).strip()
                i += 1
        else:
            i += 1

    return description, arg_descriptions

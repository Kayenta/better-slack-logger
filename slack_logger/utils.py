from __future__ import annotations

from typing import Dict, List, Optional, Union


def bold(text: str) -> str:
    return f"*{text}*"


def code(text: str) -> str:
    return f"```{text}```"


def markdown_block(markdown_text: str) -> Dict[str, Union[str, Dict[str, str]]]:
    return {"type": "section", "text": {"type": "mrkdwn", "text": markdown_text}}


def fields_block(fields: Optional[Dict[str, str]] = None) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    _fields = []
    if fields is not None:
        for key, value in fields.items():
            field_text = f'{bold(f"{key}:")} {value}'
            field_item = {"type": "mrkdwn", "text": field_text}
            _fields.append(field_item)

    return {"type": "section", "fields": _fields}


def divider_block() -> Dict[str, str]:
    return {"type": "divider"}

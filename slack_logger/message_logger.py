from __future__ import annotations

from socket import gethostname
from typing import Dict, List, Optional, Union

import slack_sdk
from yaml import dump

from .utils import bold, code, divider_block, fields_block, markdown_block


class SlackLogger:
    """
    Python message transporter for Slack
    """

    COLORS = {
        "default": "#1F2225",
        "error": "#DB2828",
        "warn": "#FBBD08",
        "info": "#2185D0",
        "verbose": "#6417C9",
        "debug": "#2185D0",
        "success": "#21BA45",
    }
    EMOJIS = {
        "default": ":mega:",
        "error": ":x:",
        "warn": ":warning:",
        "info": ":bell:",
        "verbose": ":loud_sound:",
        "debug": ":microscope:",
        "success": ":rocket:",
    }

    def __init__(
        self,
        token: str,
        *,
        service_name: Optional[str] = None,
        service_environment: Optional[str] = None,
        display_hostname: bool = True,
        default_level: Optional[str] = None,
    ):
        self.token = token
        self.service_name = service_name
        self.service_environment = service_environment

        self.host_name = gethostname() if display_hostname else None

        self.default_level = (
            default_level if self.default_level in self.COLORS.keys() else "default"
        )

        self.slack = slack_sdk.WebClient(token=self.token)

    @staticmethod
    def construct_header() -> Dict[str, Union[str, Dict[str, str]]]:
        header = "<!channel>"

        return markdown_block(header)

    @classmethod
    def construct_title(
        cls,
        title: Optional[str],
        level: str,
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        emoji = cls.EMOJIS.get(level)
        _title = bold(title) if title is not None else ""
        if emoji is not None:
            _title = f"{emoji} {_title}"

        return markdown_block(_title)

    @staticmethod
    def construct_description(description: str) -> Dict[str, Union[str, Dict[str, str]]]:
        return markdown_block(description)

    @staticmethod
    def construct_error(error: str) -> Dict[str, Union[str, Dict[str, str]]]:
        return markdown_block(f"{bold('Error:')}\n{code(error)}")

    @staticmethod
    def construct_metadata(metadata: Union[Dict, List]) -> Dict[str, Union[str, Dict[str, str]]]:
        _metadata = dump(metadata, indent=4, default_flow_style=False, sort_keys=False)

        return markdown_block(f":house_buildings: {bold('Metadata:')}\n{code(_metadata)}")

    def construct_environment(self) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        fields = {"Service": self.service_name}
        if self.host_name is not None:
            fields["Host"] = self.host_name
        if self.service_environment is not None:
            fields["Environment"] = self.service_environment

        return fields_block(_fields=fields)

    def send(
        self,
        channel: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        level: Optional[str] = None,
        error: Optional[str] = None,
        metadata: Optional[str] = None,
        tag_channel: bool = True,
    ):
        title = title or ""
        description = description or ""
        level = "error" if error is not None else level or self.default_level
        color = self.COLORS.get(level)

        # The final list of all the blocks to be sent in the notification
        blocks = []

        if tag_channel:
            header_block = self.construct_header()
            blocks.append(header_block)

        if title is not None:
            title_block = self.construct_title(title, level)
            blocks.append(title_block)

        if description is not None:
            description_block = self.construct_description(description)
            blocks.append(description_block)

        if error is not None:
            error_block = self.construct_error(error)
            blocks.append(error_block)

        if metadata is not None:
            metadata_block = self.construct_metadata(metadata)
            blocks.append(metadata_block)

        blocks.append(divider_block())

        environment_block = self.construct_environment()
        blocks.append(environment_block)

        payload = {
            "channel": channel,
            "attachments": [{"color": color, "blocks": blocks}],
        }

        return self.slack.chat_postMessage(**payload)

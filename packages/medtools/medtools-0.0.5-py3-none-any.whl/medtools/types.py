from typing import Any, Literal

from pydantic import BaseModel


class ToolResult(BaseModel):
    type: Literal["string", "json", "bytes", "error"]
    data: Any  # When the type is `file`, data should be in bytes

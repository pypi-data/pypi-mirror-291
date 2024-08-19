from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    platform: str = "linux/amd64"
    language: str
    version: str
    codebase: str
    project_setup: List[str]
    name: str

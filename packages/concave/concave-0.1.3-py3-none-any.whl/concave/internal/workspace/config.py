import hashlib
import os
from typing import List

import jinja2
from pydantic import BaseModel


class Config(BaseModel):
    name: str
    platform: str = "linux/amd64"
    arch: str = "amd64"
    language: str = "python"
    codebase: str
    repo_script_list: list[str]
    env_script_list: list[str]
    conda_profile: str

    @property
    def git_repo(self):
        parts = self.codebase.split('/')
        if len(parts) == 3:
            return self.codebase
        elif len(parts) == 5:
            return '/'.join(parts[:3])

    @property
    def git_commit(self):
        parts = self.codebase.split('/')
        if len(parts) == 3:
            return None
        elif len(parts) == 5:
            return parts[-1]

    @property
    def setup_env_script(self):
        return "\n".join(["#!/bin/bash", "set -euxo pipefail"] + self.env_script_list) + "\n"

    @property
    def install_repo_script(self):
        return "\n".join(["#!/bin/bash", "set -euxo pipefail"] + self.repo_script_list) + "\n"

    @property
    def base_image_key(self):
        return f"concave-base:latest"

    @property
    def env_image_key(self):
        """
        The key for the environment image is based on the hash of the environment script list.
        If the environment script list changes, the image will be rebuilt automatically.

        Note that old images are not automatically deleted, so consider cleaning up old images periodically.
        """
        hash_object = hashlib.sha256()
        hash_object.update(str(self.env_script_list).encode("utf-8"))
        hash_value = hash_object.hexdigest()
        val = hash_value[:22]  # 22 characters is still very likely to be unique
        return f"concave-env:{val}"

    @property
    def workspace_image_key(self):
        return f"concave-workspace-{self.name}:latest"

    @property
    def base_dockerfile(self):
        if self.arch == "arm64":
            conda_arch = "aarch64"
        else:
            conda_arch = "x86_64"
        with open(f"{os.path.dirname(__file__)}/base.Dockerfile.j2") as f:
            dockerfile = jinja2.Template(f.read()).render(
                PLATFORM=self.platform,
                CONDA_ARCH=conda_arch,
            )
        return dockerfile

    @property
    def env_dockerfile(self):
        with open(f"{os.path.dirname(__file__)}/env.Dockerfile.j2") as f:
            dockerfile = jinja2.Template(f.read()).render(
                PLATFORM=self.platform,
                CONDA_PROFILE=self.conda_profile
            )
        return dockerfile

    @property
    def workspace_dockerfile(self):
        with open(f"{os.path.dirname(__file__)}/workspace.Dockerfile.j2") as f:
            dockerfile = jinja2.Template(f.read()).render(
                PLATFORM=self.platform,
                ENV_IMAGE_NAME=self.env_image_key,
                CONDA_PROFILE=self.conda_profile
            )
        return dockerfile

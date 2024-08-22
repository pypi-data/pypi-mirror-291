from pathlib import Path
from typing import Optional, Union

import yaml
from pydantic import BaseModel, Field


class ConfigBase(BaseModel):
    class Config:
        extra = "forbid"  # Forbids extra fields in the YAML config


class EC2Config(ConfigBase):
    # EC2 config items
    instance_type: str
    ebs_volume_size: int
    key_pair_name: str
    vpc_id: Optional[str] = None
    managed_policies: Optional[list] = Field(default_factory=list)
    custom_policy: Optional[dict] = Field(default_factory=dict)


class UserDataConfig(ConfigBase):
    python_version: str
    git_user_name: str
    git_user_email: str


class EnvironmentConfig(ConfigBase):
    account: str
    region: str


class EC2StackConfig(ConfigBase):
    stack_id: str
    base_resource_name: str

    ec2: EC2Config
    user_data: UserDataConfig
    environment: EnvironmentConfig

    @classmethod
    def load_from_file(cls, file_path: Union[Path, str]) -> "EC2StackConfig":
        with open(file_path, "r") as file:
            config_data = yaml.safe_load(file)
        return cls.model_validate(config_data)

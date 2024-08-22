from pathlib import Path
from typing import Union

import aws_cdk as cdk

from ec2_dev_machine.cdk.ec2_stack import EC2InstanceProps, EC2InstanceStack
from ec2_dev_machine.config import EC2StackConfig
from ec2_dev_machine.user_data.user_data import generate_user_data_script


class DevMachine:
    def __init__(self, config_file_path: Union[Path, str]):
        self.config = EC2StackConfig.load_from_file(config_file_path)
        user_data_script = generate_user_data_script(self.config.user_data)

        self.app = cdk.App()

        environment = cdk.Environment(**self.config.environment.model_dump())
        ec2_stack_props = EC2InstanceProps(
            base_resource_name=self.config.base_resource_name,
            init_script=user_data_script,
            **self.config.ec2.model_dump()
        )

        self.stack = EC2InstanceStack(
            self.app,
            stack_id=self.config.stack_id,
            properties=ec2_stack_props,
            env=environment,
        )

    def synth(self):
        self.app.synth()


# TODO: Add CLI interface for this

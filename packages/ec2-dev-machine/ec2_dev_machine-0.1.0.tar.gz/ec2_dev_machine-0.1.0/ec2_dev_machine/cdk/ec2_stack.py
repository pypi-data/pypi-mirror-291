from typing import Any, Optional

from aws_cdk import CfnOutput, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct
from pydantic import BaseModel, Field


class EC2InstanceProps(BaseModel):
    base_resource_name: str
    instance_type: str
    ebs_volume_size: int
    key_pair_name: str
    managed_policies: list[str] = Field(default_factory=list)
    custom_policy: dict = Field(default_factory=dict)
    vpc_id: Optional[str] = None
    init_script: Optional[str] = None


class EC2InstanceStack(Stack):
    def __init__(self, scope: Construct, stack_id: str, properties: EC2InstanceProps, **kwargs: Any) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self._properties = properties
        self.base_resource_name = self._properties.base_resource_name

        if properties.vpc_id:
            vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=self._properties.vpc_id)
        else:
            # Create Basic VPC
            vpc = ec2.Vpc(
                scope=self,
                id=f"{self.base_resource_name}-vpc",
                max_azs=2,
                subnet_configuration=[
                    ec2.SubnetConfiguration(
                        name="public-subnet-1",
                        subnet_type=ec2.SubnetType.PUBLIC,
                        cidr_mask=24,
                    ),
                    ec2.SubnetConfiguration(
                        name="public-subnet-2",
                        subnet_type=ec2.SubnetType.PUBLIC,
                        cidr_mask=24,
                    ),
                ],
            )

        # Create Security Group
        security_group = ec2.SecurityGroup(
            scope=self,
            id=f"{self.base_resource_name}-sg",
            vpc=vpc,
            allow_all_outbound=True,
        )

        # Create role
        self.instance_role = iam.Role(
            scope=self,
            id=f"{self.base_resource_name}-instance-role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )

        # Attach SSM managed policy
        self.instance_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )
        for managed_policy in self._properties.managed_policies:
            self.instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy))

        if self._properties.custom_policy:
            custom_policy_document = iam.PolicyDocument.from_json(self._properties.custom_policy)

            _ = iam.Policy(
                self, id=f"{self.base_resource_name}-policy", document=custom_policy_document
            ).attach_to_role(self.instance_role)

        instance_type = ec2.InstanceType(self._properties.instance_type)

        image_ami = ec2.MachineImage.latest_amazon_linux2023(
            cpu_type=ec2.AmazonLinuxCpuType[instance_type.architecture.value]
        )

        self.key_pair = ec2.KeyPair.from_key_pair_name(
            scope=self,
            id=f"{self.base_resource_name}-key-pair",
            key_pair_name=self._properties.key_pair_name,
        )

        self.instance = ec2.Instance(
            scope=self,
            id=f"{self.base_resource_name}-instance",
            instance_type=instance_type,
            machine_image=image_ami,
            key_pair=self.key_pair,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=self._properties.ebs_volume_size,
                        encrypted=True,
                        volume_type=ec2.EbsDeviceVolumeType.GP3,
                    ),
                ),
            ],
            security_group=security_group,
            associate_public_ip_address=True,
            role=self.instance_role,
            user_data=ec2.UserData.custom(self._properties.init_script),
        )

        # Output Instance ID
        CfnOutput(self, "InstanceId", value=self.instance.instance_id)

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    LegacyStackSynthesizer,
)
from constructs import Construct

class MVCDK(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        kwargs["synthesizer"] = LegacyStackSynthesizer()
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        role = iam.Role.from_role_arn(
            self, "LabRole",
            "arn:aws:iam::767397918581:role/LabRole",
            mutable=False
        )

        sg = ec2.SecurityGroup(self, "InstanceSG",
            vpc=vpc,
            description="Permitir SSH y HTTP",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        ec2.Instance(self, "NuevaMVCDK",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({
                "us-east-1": "ami-043cbf1cf918dd74f"
            }),
            vpc=vpc,
            key_name="vockey",
            security_group=sg,
            role=role,
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )]
        )
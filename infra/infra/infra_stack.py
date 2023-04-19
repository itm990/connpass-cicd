import os

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets,
)
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "Vpc", max_azs=3)

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        asset = ecr_assets.DockerImageAsset(self, "petgram",
            directory=os.path.join(os.getcwd(), "../app")
        )

        ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
            cluster=cluster,
            cpu=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_docker_image_asset(asset)),
            memory_limit_mib=2048,
            public_load_balancer=True)
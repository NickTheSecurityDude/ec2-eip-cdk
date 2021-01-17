#!/usr/bin/env python3

from aws_cdk import core

import boto3
import sys


client = boto3.client('sts')

region=client.meta.region_name

#if region != 'us-east-1':
#  print("This app may only be run from us-east-1")
#  sys.exit()

account_id = client.get_caller_identity()["Account"]

my_env = {'region': region, 'account': account_id}

from stacks.iam_stack import IAMStack
from stacks.sg_stack import SGStack
from stacks.ec2_stack import EC2Stack

proj_name="linprod-mngsrv"

app = core.App()

iam_stack=IAMStack(app, proj_name+"-iam",env=my_env)
sg_stack=SGStack(app, proj_name+"-sg",env=my_env)
ec2_stack=EC2Stack(app, proj_name+"-ec2",
  imaging_sg=sg_stack.imaging_sg,
  imaging_ec2_role=iam_stack.imaging_ec2_role,
  env=my_env
)

for stack in [iam_stack,sg_stack,ec2_stack]:
  core.Tags.of(stack).add("Project", proj_name)

app.synth()

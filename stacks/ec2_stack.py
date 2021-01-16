##############################################################
#
# ec2_stack.py
#
#
##############################################################

from aws_cdk import (
  aws_ec2 as ec2,
  aws_iam as iam,
  core
)

class EC2Stack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, imaging_sg: ec2.ISecurityGroup, imaging_ec2_role: iam.IRole, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # elastic ip
    eip=ec2.CfnEIP(self,"Imaging Server IP")

    core.Tags.of(eip).add(key="Name",value="Imaging Server EIP")

    # imaging ec2 instance

    #ami_id=ssm.StringParameter.value_from_lookup(self,"/linux/production/ami_id")

    itype=ec2.InstanceType("t3.nano")
    iami=ec2.MachineImage.from_ssm_parameter("/linux/production/ami_id",os=ec2.OperatingSystemType.LINUX)
    default_vpc=ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)

    imaging_ec2=ec2.Instance(self, "ec2-instance",
      instance_type = itype,
      machine_image = iami,
      vpc = default_vpc,
      security_group=imaging_sg,
      role=imaging_ec2_role
    )

    # add tags
    core.Tags.of(imaging_ec2).add(key="Name",value="Linux-Prod-Imaging-Server")
    core.Tags.of(imaging_ec2).add(key="ami_id_parameter",value="/linux/production/ami_id")
    core.Tags.of(imaging_ec2).add(key="OS",value="linux")
    core.Tags.of(imaging_ec2).add(key="ServerGroup",value="production")
    core.Tags.of(imaging_ec2).add(key="Type",value="imaging_server")

    # attach eip
    ec2.CfnEIPAssociation(self,"EIP Attachment",eip=eip.ref,instance_id=imaging_ec2.instance_id)

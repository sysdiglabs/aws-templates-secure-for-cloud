# Sysdig Agentless Role Provisioning for AW Organization

## Usage

1. Before launching StackSet you will need a pre-provisioning on Sysdig Cloud
Review `./sysdig_provisioning.sh` and get `SysdigTrustedEntity` and `ExternalId` values for next step.

2. Launch StackSet
[Cloudformation Stacksets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html) will be used
>  Using an administrator account, you define and manage an AWS CloudFormation template, and use the template as the basis for provisioning stacks into selected target accounts across specified AWS Regions.

- [Prerequisites for stack set operations](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs.html)
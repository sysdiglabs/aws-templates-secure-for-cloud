# Decision Record

## 2022.05.13 - organizational/multi-account deployment method

https://github.com/sysdiglabs/aws-templates-secure-for-cloud/pull/77

client needs to deploy things on different levels of accounts
1. management account, requires the creation of a SysdiRole to be able to get organizational cloudtrail data (+s3,sns)
2. all member accounts, require the creation of a SysdigAgentlessRole for benchmark
3. sysdig workload (ecs,apprunner or eks) must be deployed

each requirement is separated on its own `Stack` and put all together on a `Stackset` within the [organizational-setup](./organizational_setup) use-case
We use the [`AWS::CloudFormation::StackSet` `StackInstancesGroup.DeploymentTargets`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-deploymenttargets)
attribute to configure where to deploy what.


## 2022.05.13 - organizational/manual sysdig pre-setup - bash scripts

https://github.com/sysdiglabs/aws-templates-secure-for-cloud/pull/77

for Compliance feature, on self-baked use-cases (which are not launched from the Sysdig Onboarding page)
a pre-setup must be made for the [Organizational AgentlessRole](./organizational_agentless_role)

a setup guide is given to the client to execute manually (sysdig provisioning > aws provisioning > validation)
Options to automatize this I researched are
- https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html

think these options would only complicate things (bash script maintenance and troubleshooting)
not worthy automatizing



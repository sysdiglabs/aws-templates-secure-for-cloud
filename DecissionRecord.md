# Decision Record

## 2. organizational; multi-account deployment method

client needs to deploy things on different levels of accounts
1. management account, requires the creation of a SysdiRole to be able to get organizational cloudtrail data (+s3,sns)
2. all member accounts, require the creation of a SysdigAgentlessRole for benchmark
3. sysdig workload (ecs,apprunner or eks) must be deployed

three different Cloudformation templates are prepared
1. [Management Account SysdigRole](./organizational_management_account) Stack
2. [Organizational AgentlessRole](./organizational_agentless_role) Stackset
3. Sysdig Workload Deployment will be launched ad-hoc


## 1. organizational; manual sysdig pre-setup - bash scripts

for Compliance feature, on self-baked use-cases (which are not launched from the Sysdig Onboarding page)
a pre-setup must be made for the [Organizational AgentlessRole](./organizational_agentless_role)

a setup guide is given to the client to execute manually (sysdig provisioning > aws provisioning > validation)
Options to automatize this I researched are
- https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html

think these options would only complicate things (bash script maintenance and troubleshooting)
not worthy automatizing



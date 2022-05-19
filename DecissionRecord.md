# Decision Record

## 2022.05.19 - helm chart deployment

Analysed possible ways of deploying things into k8s through cloudformation.
Not official but aws-quickstart team offers cloudformation [AWSQS::Kubernetes::Helm](https://github.com/aws-quickstart/quickstart-helm-resource-provider/blob/main/README.md) cloudformation resource.

Resolution: not implemented due to client not needing cloudformation, due to using Spinnaker for Helm deployments.


## 2022.05.13 - organizational/multi-account deployment method

https://github.com/sysdiglabs/aws-templates-secure-for-cloud/pull/77

client needs to deploy things on different levels of accounts
1. management account, requires the creation of a SysdiRole to be able to get organizational cloudtrail data (+s3,sns)
2. all member accounts, require the creation of a SysdigAgentlessRole for benchmark
3. sysdig workload (ecs,apprunner or eks) must be deployed on a selected member account.

Each requirement is separated on its own `Stack` and put all together on a `Stackset` 
We can make use the [`AWS::CloudFormation::StackSet` `StackInstancesGroup.DeploymentTargets`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-deploymenttargets)
attribute to configure where (org unit or account) to deploy what.

Resolution: none of this is developed yet, because client did not need cloudformation in the end we just delivered a use-case.


## 2022.05.13 - organizational/manual sysdig pre-setup - bash scripts

https://github.com/sysdiglabs/aws-templates-secure-for-cloud/pull/77

for Compliance feature, on self-baked use-cases (which are not launched from the Sysdig Onboarding page)
a pre-setup must be made on Sysdig Secure backend for cloud-account(s) and compliance task provisioning.

a setup guide is given to the client to execute manually (1. sysdig provisioning > 2. aws provisioning > 3. validation)
Options to automatize this I researched are
- https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html

Think these options would only complicate things (bash script maintenance and troubleshooting), not worthy automatizing.

Resolution: we will provide a utility script to handle this from outside cloudformation templates.



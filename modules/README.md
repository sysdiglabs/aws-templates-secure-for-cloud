# Sysdig Secure - Modular Templates

Modular templates support cross sections of Sysdig Secure feature sets. Each template is intended to be installable alongside one another, and amongst multiple instances. 

## Common parameters

* `NameSuffix` - a unique string suffix given to named resources where applicable.
* `TrustedIdentity` - a Sysdig owned identity trusted to assume a permission limited customer installed role
* `ExternalID` - a Sysdig assigned value

## Organizations

Organizations are supported by setting the following template parameters
* `IsOrganizational=true`

### Organizational Install Configurations

Following are the new parameters to configure organizational deployments on the cloud for Sysdig Secure for Cloud :-
1. `RootOUID` - Root Organization Unit ID
2. `IncludeOUIDs` - List of AWS Organizational Unit IDs to deploy the Sysdig Secure for Cloud resources in.
3. `IncludeAccounts` - List of AWS Accounts to deploy the Sysdig Secure for Cloud resources in.
4. `ExcludeAccounts` - List of AWS Accounts to exclude deploying the Sysdig Secure for Cloud resources in.

**DEPRECATION NOTICE**: module template parameter `OrganizationalUnitIDs` has been DEPRECATED and is no longer supported. Please work with Sysdig to migrate your CFT based installs to use `IncludeOUIDs` instead to achieve the same deployment outcome.

## Available Templates

### foundational.cft.yaml
Deploys foundational Sysdig Secure resources including posture management and onboarding capabilities.
- **Components**: Secure posture, secure onboarding

### foundational_with_scanning.cft.yaml
All-in-one template combining foundational resources with both VM workload scanning and agentless volume access/scanning capabilities.
- **Components**: Secure posture, secure onboarding, VM workload scanning, secure scanning
- **Additional Parameters**: 
  - `LambdaScanningEnabled` - Enable Lambda function scanning (default: false)
  - `ScanningAccountID` - The AWS Account ID of the Sysdig Scanning Account (default: 878070807337)
  - `Regions` - Comma-separated list of regions enabled for Sysdig Scanning

### foundational_vm_workload_scanning.cft.yaml
Combines foundational resources with VM workload scanning capabilities.
- **Components**: Secure posture, secure onboarding, VM workload scanning
- **Additional Parameters**:
  - `LambdaScanningEnabled` - Enable Lambda function scanning (default: false)

### foundational_volume_access.cft.yaml
Combines foundational resources with agentless volume access and scanning capabilities.
- **Components**: Secure posture, secure onboarding, secure scanning
- **Additional Parameters**:
  - `ScanningAccountID` - The AWS Account ID of the Sysdig Scanning Account (default: 878070807337)
  - `Regions` - Comma-separated list of regions enabled for Sysdig Scanning

### volume_access.cft.yaml
Standalone template for agentless volume access and scanning capabilities.

### vm_workload_scanning.cft.yaml
Standalone template for VM workload scanning capabilities.

### log_ingestion.events.cft.yaml, log_ingestion.legacy_events.cft.yaml, log_ingestion.s3.cft.yaml
Templates for configuring log ingestion through EventBridge and S3.

### response_actions.cft.yaml
Template for deploying Sysdig response actions capabilities.

## Testing Steps

### 1. Verify GitHub Actions Publish Templates Check
From the development PR on `aws-templates-secure-for-cloud`, ensure the **GH Action Publish Templates** check passes.

### 2. Verify Template Upload to S3
Once the GitHub Action passes, expand the action details and verify that the make run for the corresponding template YAML with the changes was copied to the S3 location.

**Expected Output Example:**
```
upload: ./foundational.cft.yaml to s3://cf-templates-cloudvision-ci/modules/pr/165/foundational.cft.yaml
aws s3 cp log_ingestion.s3.cft.yaml s3://cf-templates-cloudvision-ci/modules/pr/165/log_ingestion.s3.cft.yaml
Completed 12.6 KiB/12.6 KiB (21.0 KiB/s) with 1 file(s) remaining
```

### 3. Test Template via Sysdig UI
To test the template, run the CFT Onboarding flow from the Sysdig UI:

1. **Launch Stack with PR Template**
   - In the Sysdig UI, click "Launch Stack"
   - The wizard defaults to the latest pinned CFT Quick Create URL
   - Edit the URL to use the PR template from step 2

2. **Update Template URL**
   - Replace the version path from the default pinned version (e.g., `/v3.1.0/`) with the PR path (e.g., `/pr/165/`)
   
   **Example:**
   - Default: `templateURL=https%3A%2F%2Fcf-templates-cloudvision-ci.s3.eu-west-1.amazonaws.com%2Fmodules%2Fv3.1.0%2Ffoundational.cft.yaml`
   - PR: `templateURL=https%3A%2F%2Fcf-templates-cloudvision-ci.s3.eu-west-1.amazonaws.com%2Fmodules%2Fpr%2F165%2Ffoundational.cft.yaml`

3. **Verify Template URL in AWS Console**
   - Refresh the page
   - Confirm the template URL is updated on the AWS console
   - Expected Template URL: `https://cf-templates-cloudvision-ci.s3.eu-west-1.amazonaws.com/modules/pr/165/foundational.cft.yaml`

4. **Create Stack**
   - Click "Create Stack" on AWS console
   - Ensure the creation of StackSets with the PR template is successful

### 4. Complete E2E Onboarding Test
Once stack creation is successful:

1. Return to the Sysdig UI
2. Click "Complete Onboarding" to finish Sysdig side provisioning
3. Verify all accounts are onboarded with the expected features
4. Confirm post-onboarding health validation checks pass

### Validation Criteria
The CFT changes are successfully tested and ready to merge when:
- ✅ GitHub Actions Publish Templates check passes
- ✅ Templates are uploaded to correct S3 PR location
- ✅ PR template URL works in AWS CloudFormation console
- ✅ StackSets are created successfully with PR template
- ✅ All accounts onboard with expected features
- ✅ Post-onboarding health validation checks pass


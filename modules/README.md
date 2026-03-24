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

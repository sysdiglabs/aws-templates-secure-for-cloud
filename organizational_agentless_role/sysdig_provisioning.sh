#!/bin/bash

# usage
# 1. configure api token
SYSDIG_API_TOKEN=

# 2. set this value to false
doCleanup=true

SYSDIG_ENDPOINT=https://secure.sysdig.com
SYSDIG_AGENTLESS_ROLE_NAME=SysdigAgentlessRole

accounts=()
taskId=
externalId=
trustedIdentity=


fetchOrganizationAccounts(){
  echo "-- Fetching Organization Accounts"
  for accountId in $(aws organizations list-accounts | jq ".Accounts|.[]|.Id|tonumber"); do
    echo $accountId
    accounts+=($accountId)
  done
}


createSysdigCloudAccounts(){
  echo "-- Create Sysdig CloudAccounts (n)"
  for accountId in "${accounts[@]}"
  do
    curl "$SYSDIG_ENDPOINT/api/cloud/v2/accounts?includeExternalID=true\&upsert=true" \
    --header "Authorization: Bearer $SYSDIG_API_TOKEN" \
    -X POST \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
          "accountId": "'$accountId'",
          "provider": "aws",
          "roleAvailable": true,
          "roleName": "'$SYSDIG_AGENTLESS_ROLE_NAME'"
       }'
  done
}

createSysdigTask(){
  echo "-- Creating task"

  accountIdTxt=
  for accountId in "${accounts[@]}"
  do
    accountIdTxt="$accountIdTxt\\\""$accountId\\\"","
  done
  accountIdTxt=${accountIdTxt:0:${#accountIdTxt}-1}

  taskId=$(curl -s "$SYSDIG_ENDPOINT/api/benchmarks/v2/tasks" \
  --header "Authorization: Bearer $SYSDIG_API_TOKEN" \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
      "name": "Sysdig Secure for Cloud (AWS) - Organization",
      "schedule": "0 3 * * *",
      "schema": "aws_foundations_bench-1.3.0",
      "scope": "aws.accountId in ('"$accountIdTxt"')",
      "enabled": true
    }' | jq '.id')
    echo "Created task with Id: $taskId"
}

getTrustIdentity(){
  echo "-- Fetching SysdigTrustedIdentity"
  trustedIdentity=$(curl -s "$SYSDIG_ENDPOINT/api/cloud/v2/aws/trustedIdentity" \
  --header "Authorization: Bearer $SYSDIG_API_TOKEN")
  echo $trustedIdentity
}

getExternalId(){
  echo "-- Fetching ExternalId"
  externalId=$(curl -s "$SYSDIG_ENDPOINT/api/cloud/v2/accounts/${accounts[0]}?includeExternalId=true" \
  --header "Authorization: Bearer $SYSDIG_API_TOKEN" | jq ".externalId")
  echo $externalId
}

listSysdigCloudAccounts(){
  echo "-- List accounts"
  curl -s "$SYSDIG_ENDPOINT/api/cloud/v2/accounts" \
  --header "Authorization: Bearer $SYSDIG_API_TOKEN" | jq ".[]|.accountId"
}

listSysdigTasks(){
  echo "-- List tasks"
  curl -s "$SYSDIG_ENDPOINT/api/benchmarks/v2/tasks" \
  --header "Authorization: Bearer $SYSDIG_API_TOKEN" | jq ".[]|.id"
}

deleteSysdigCloudAccount(){
  echo "-- Deleting Sysdig CloudAccounts (n)"
  for accountId in "${accounts[@]}"
  do
    curl "$SYSDIG_ENDPOINT/api/cloud/v2/accounts/$accountId" \
    --header "Authorization: Bearer $SYSDIG_API_TOKEN" \
    -X DELETE
  done
}

deleteSysdigTask(){
  echo "-- Delete SysdigTag"
  curl -s "$SYSDIG_ENDPOINT/api/benchmarks/v2/tasks/$taskId" \
  --header "Authorization: Bearer $SYSDIG_API_TOKEN" \
  -X DELETE
}


#
# main
#

fetchOrganizationAccounts
listSysdigCloudAccounts | sort > sysdig_initial

createSysdigCloudAccounts
listSysdigCloudAccounts | sort > sysdig_post_upsert
echo "-- Creation Diff"
diff sysdig_initial sysdig_post_upsert


listSysdigTasks > sysdig_task_initial
createSysdigTask
listSysdigTasks > sysdig_task_post_insert
echo "-- Creation Diff"
diff sysdig_task_initial sysdig_task_post_insert

echo
echo
echo "###################################################"
echo "####### GET THIS VALUES FOR AWS PROVISIONING #####"
getExternalId
echo
getTrustIdentity
echo
echo
echo "###################################################"

if [ $doCleanup == true ]; then
  echo "--- Cleanup SysdigCloudAccount"
  deleteSysdigCloudAccount
  listSysdigCloudAccounts | sort > sysdig_post_delete
  echo "-- Cleanup Diff"
  diff sysdig_initial sysdig_post_delete

  echo "-- Cleanup SysdigTask"
  deleteSysdigTask
  listSysdigTasks > sysdig_task_post_delete
  echo "-- Cleanup Diff"
  diff sysdig_task_initial sysdig_task_post_delete
fi
rm sysdig_initial sysdig_post_upsert sysdig_post_delete
echo
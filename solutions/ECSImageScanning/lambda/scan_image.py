import boto3
import json
import os


def handler(event, context, client=boto3.client('codebuild')):
    if event is not None and "detail" in event and "containers" in event["detail"]:
        account = event["account"]
        region = event["region"]

        task_definition_arn = event["detail"]["taskDefinitionArn"]
        images = ((container["image"], container["name"]) for container in event["detail"]["containers"] if "image" in container)
        for image, name in images:
            print("Checking image " + image + " for task " + task_definition_arn)
            secret_id = _get_credentials_secret_for(task_definition_arn, image, name)
            variables = [
                    _plaintext_variable("ACCOUNT", account),
                    _plaintext_variable("REGION", region),
                    _plaintext_variable("REPOSITORY", image)
                ]

            if secret_id:
                variables.extend([
                    _secret_manager_variable("DOCKER_USER", secret_id, "username"),
                    _secret_manager_variable("DOCKER_PASS", secret_id, "password"),
                ])

            client.start_build(
                projectName=os.getenv("CODE_BUILD_PROJECT_NAME"),
                environmentVariablesOverride=variables
            )


def _get_credentials_secret_for(task_definition_arn, image, name):
    client = boto3.client('ecs')
    task_definition = client.describe_task_definition(taskDefinition=task_definition_arn)
    for container in task_definition["taskDefinition"]["containerDefinitions"]:
        if container["image"] == image \
            and container["name"] == name \
            and "repositoryCredentials" in container \
            and "credentialsParameter" in container["repositoryCredentials"]:
                return container["repositoryCredentials"]["credentialsParameter"]
    return None

def _plaintext_variable(name, value):
    return {
        'name': name,
        'value': value,
        'type': 'PLAINTEXT'
    }

def _secret_manager_variable(name, secret, key):
    return {
        'name': name,
        'value': secret + ":" + key,
        'type': 'SECRETS_MANAGER'
    }

import boto3
import os


def handler(event, context, client=boto3.client('codebuild')):
    if event is not None and "detail" in event and "containers" in event["detail"]:
        account = event["account"]
        region = event["region"]

        images = (container["image"] for container in event["detail"]["containers"] if "image" in container)
        for image in images:
            client.start_build(
                projectName=os.getenv("CODE_BUILD_PROJECT_NAME"),
                environmentVariablesOverride=[
                    _plaintext_variable("ACCOUNT", account),
                    _plaintext_variable("REGION", region),
                    _plaintext_variable("REPOSITORY", image),
                ]
            )


def _plaintext_variable(name, value):
    return {
        'name': name,
        'value': value,
        'type': 'PLAINTEXT'
    }

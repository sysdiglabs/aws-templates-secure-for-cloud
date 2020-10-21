from doublex import *
from doublex_expects import *
from expects import *
from mamba import *

from trigger_scan import handler, CODE_BUILD_PROJECT_NAME

with description("Inline Scanning Trigger") as self:
    with before.each:
        self.client = Spy()

    with it("is able to trigger the build to CodeBuild"):
        handler(self.ecs_running_task_event(), None, self.client)

        expect(self.client.start_build).to(have_been_called_with(
            projectName=CODE_BUILD_PROJECT_NAME,
            environmentVariablesOverride=contain(have_keys(value="sysdig/agent")))
        )
        expect(self.client.start_build).to(have_been_called_with(
            projectName=CODE_BUILD_PROJECT_NAME,
            environmentVariablesOverride=contain(have_keys(value="alpine")))
        )
        expect(self.client.start_build).to(have_been_called.twice)


    def ecs_running_task_event(self):
        return {
            "version": "0",
            "id": "0000000",
            "detail-type": "ECS Task State Change",
            "source": "aws.ecs",
            "account": "000000000",
            "time": "2020-08-31T10:44:04Z",
            "region": "eu-west-3",
            "resources": [
                "arn:aws:ecs:eu-west-3:000000000:task/36e745f7-8a16-46e2-9485-0620c1b986da"
            ],
            "detail": {
                "attachments": [
                    {
                        "id": "8b8065a5-ea82-4463-b8bb-b8e4c988ef44",
                        "type": "eni",
                        "status": "PRECREATED",
                        "details": [
                            {
                                "name": "subnetId",
                                "value": "subnet-04dd0b8206818d704"
                            }
                        ]
                    }
                ],
                "availabilityZone": "eu-west-3a",
                "clusterArn": "arn:aws:ecs:eu-west-3:000000000:cluster/test-ecs-events",
                "containers": [
                    {
                        "containerArn": "arn:aws:ecs:eu-west-3:000000000:container/b2fe579b-d269-4ecb-8337-7635a8fce144",
                        "lastStatus": "PENDING",
                        "name": "sysdig-agent",
                        "image": "sysdig/agent",
                        "taskArn": "arn:aws:ecs:eu-west-3:000000000:task/36e745f7-8a16-46e2-9485-0620c1b986da",
                        "networkInterfaces": [],
                        "cpu": "0"
                    },
                    {
                        "containerArn": "arn:aws:ecs:eu-west-3:000000000:container/b2fe579b-d269-4ecb-8337-7635a8fce144",
                        "lastStatus": "PENDING",
                        "name": "alpine",
                        "image": "alpine",
                        "taskArn": "arn:aws:ecs:eu-west-3:000000000:task/36e745f7-8a16-46e2-9485-0620c1b986da",
                        "networkInterfaces": [],
                        "cpu": "0"
                    }
                ],
                "createdAt": "2020-08-31T10:44:04.787Z",
                "launchType": "FARGATE",
                "cpu": "1024",
                "memory": "2048",
                "desiredStatus": "RUNNING",
                "group": "family:fargate-sysdig-agent",
                "lastStatus": "PROVISIONING",
                "overrides": {
                    "containerOverrides": [
                        {
                            "name": "sysdig-agent"
                        }
                    ]
                },
                "updatedAt": "2020-08-31T10:44:04.787Z",
                "taskArn": "arn:aws:ecs:eu-west-3:000000000:task/36e745f7-8a16-46e2-9485-0620c1b986da",
                "taskDefinitionArn": "arn:aws:ecs:eu-west-3:000000000:task-definition/fargate-sysdig-agent:1",
                "version": 1,
                "platformVersion": "1.3.0"
            }
        }

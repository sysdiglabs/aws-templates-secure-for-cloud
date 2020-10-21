import os

import sdcclient
from doublex import *
from doublex_expects import *
from expects import expect, be_true
from mamba import description, it, context, before

from scan_image import handler, handler_with_client

with description('Backend Scanning from ECS') as self:
    with context('when receiving an event from ECS'):
        with before.each:
            self.scanning_client = sdcclient.SdScanningClient(os.getenv("SECURE_API_TOKEN"))
            self.dummy_client = Spy()
            when(self.dummy_client).add_image(ANY_ARG).returns((True, []))

        with it('scans the image specified in the event'):
            images = ['sysdig/agent', 'alpine']

            handler(self.ecs_running_task_event(), None)

            expect(self.scanning_client.get_image(images[0])[0]).to(be_true)
            expect(self.scanning_client.get_image(images[1])[0]).to(be_true)

        with it('is called with the correct parameters'):
            images = ['sysdig/agent', 'alpine']

            handler_with_client(self.ecs_running_task_event(), None, self.dummy_client)

            expect(self.dummy_client.add_image).to(have_been_called_with(images[0]))
            expect(self.dummy_client.add_image).to(have_been_called_with(images[1]))
            expect(self.dummy_client.add_image).to(have_been_called.twice)



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

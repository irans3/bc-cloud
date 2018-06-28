import boto3
import os

fname = 'FirstRegionalInstances.json'

with open(fname, 'r') as f:
    template_body = f.read()

response = client.create_stack(
    StackName='FirstRegionalInstances',
    TemplateURL='https://aws-quickstart.s3.amazonaws.com/quickstart-linux-bastion/templates/linux-bastion-master.template'
    DisableRollback=False,
    ResourceTypes=[
        'AWS::EC2::*',
    ],
    RoleARN='string',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'string'
        },
    ],
    ClientRequestToken='string',
    EnableTerminationProtection=False
)
response

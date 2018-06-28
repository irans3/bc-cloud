#!/usr/bin/env python
# Create bastions in multiple regions using AWS quickstart.
import boto3
from ast import literal_eval


def bastion_popup(fname='regions.json'):
    
    with open(fname, 'r') as f:
        regions = literal_eval(f.read())

    for key, value in regions.items():
        # Setup.
        session = boto3.session.Session(region_name=value)
        ec2client = session.client('ec2')
        cf_client = session.client('cloudformation')

        az = ec2client.describe_availability_zones()['AvailabilityZones']
        print(az[0]['ZoneName'], az[1]['ZoneName'])

        # Work.
        response = cf_client.create_stack(
            StackName='LocalBastion',
            TemplateURL='https://aws-quickstart.s3.amazonaws.com/quickstart-linux-bastion/templates/linux-bastion-master.template',
            Parameters=[
                {
                    'ParameterKey': 'KeyPairName',
                    'ParameterValue': key + '-dev'
                },
                {
                    'ParameterKey': 'BastionAMIOS',
                    'ParameterValue': 'Ubuntu-Server-16.04-LTS-HVM'
                },
                {
                    'ParameterKey': 'BastionInstanceType',
                    'ParameterValue': 't2.micro'
                },
                {
                    'ParameterKey': 'EnableX11Forwarding',
                    'ParameterValue': 'true'
                },
                {
                    'ParameterKey': 'KeyPairName',
                    'ParameterValue': key + '-dev'
                },
                {
                    'ParameterKey': 'AvailabilityZones',
                    # Assumes at least two AZs.
                    'ParameterValue': ','.join([az[0]['ZoneName'], az[1]['ZoneName']])
                },
                {
                    'ParameterKey': 'RemoteAccessCIDR',
                    'ParameterValue': '147.81.1.10/32'
                }
            ],
            Capabilities=[
                'CAPABILITY_IAM'
            ],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': key + '-start'
                },
            ]
        )
        print(response['StackId'])

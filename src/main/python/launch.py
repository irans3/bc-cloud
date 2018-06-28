#!/usr/bin/env python
# Generate the pem files.
import pandas as pd
import boto3

def delete_vpc(id='vpc-0417da42b96268f01', region_id='us-east-1'):
    ec2client = boto3. \
                session. \
                Session(region_name=region_id). \
                client('ec2')
    VpcId = 'vpc-0417da42b96268f01'
    subnets = ec2client.describe_subnets()
    marked_subnets = [subnet['SubnetId'] for subnet in subnets if subnet['VpcId'] == VpcId]
#    RouteTableId='rtb-029cc312c23d4ae20'
    # IgwId = 'igw-0ae2213cb7ef80bce'
    route_tables = ec2client.describe_route_tables()['RouteTables']
    marked_route_tables = [x['RouteTableId'] for x in route_tables if x['VpcId'] == VpcId]


def launch(region_id='us-east-1', region_name='us'):

    ec2client = boto3. \
                session. \
                Session(region_name=region_id). \
                client('ec2')
    response = ec2client.create_launch_template(
        DryRun=False,
        LaunchTemplateName='bastion',
        VersionDescription='string',
        LaunchTemplateData={
            'NetworkInterfaces': [
                {
                    'AssociatePublicIpAddress': True,
                    'Groups': [
                        'sg-00f444b6d942e90fe',
                    ],
                    'SubnetId': 'subnet-062568d592574414c'
                },
            ],
            'ImageId': 'ami-41e9c52e',
            'InstanceType': 't2.micro',
            'KeyName': 'us-dev',
            'Monitoring': {
                'Enabled': True
            },
            'DisableApiTermination': False,
            'InstanceInitiatedShutdownBehavior': 'stop',
            'UserData': '',
            'TagSpecifications': [
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'bastion'
                        },
                    ]
                },
            ],
            'CreditSpecification': {
                'CpuCredits': 'standard'
            }
        }
    )
    print(response)
    
    resp = ec2client.run_instances(
        LaunchTemplate={'LaunchTemplateId': response['LaunchTemplateId']},
        MinCount=1,
        MaxCount=1
    )

    
def main():
    response = launch()
    print(response)

    
if __name__=='__main__':
    main()

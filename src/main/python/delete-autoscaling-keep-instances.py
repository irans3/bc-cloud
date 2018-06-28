#!/usr/bin/env python

import boto3
from ast import literal_eval


def get_regions(fname='name-regions.json'):

    with open(fname, 'r') as f:
        return literal_eval(f.read())

    
def autoscaling_delete(asClient):
    
        asg_name = asClient.describe_auto_scaling_groups()['AutoScalingGroups'][0]['AutoScalingGroupName']

        response = asClient.delete_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            ForceDelete=True
        )

        
def add_bastion(region_name, region_id, ami='ami-41e9c52e', instance_type='t2.micro'):

    ec2client = boto3.session.Session(region_name=region_id).client('ec2')
    
    response = client.create_launch_template(
        DryRun=False,
        LaunchTemplateName='bastion-launch',
        LaunchTemplateData={
            'KernelId': 'string',
            'EbsOptimized': False,
            'NetworkInterfaces': [
                {
                    'AssociatePublicIpAddress': True,
                    'DeleteOnTermination': True,
                    'Groups': [
                        'string',
                    ],
                    'SubnetId': 'string'
                },
            ],
            'ImageId': 'string',
            'InstanceType': 't2.micro',
            'KeyName': region_name + '-dev',
            'InstanceInitiatedShutdownBehavior': 'stop',
            'UserData': 'string',
            'TagSpecifications': [
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': region_name + '-bastion'
                        },
                    ]
                },
            ],
            'SecurityGroupIds': [
                'string',
            ],
            'SecurityGroups': [
                'string',
            ],
        }
        )


def add_bastion_regional(regions):
    for key, value in regions.items():
        add_bastion(key, value)

    
# Delete the first Autoscaling Group in each region.
def autoscaling_delete_regional(regions):
    for region in regions.values():
        asClient = boto3.session.Session(region_name=value).client('autoscaling')
        autoscaling_delete(asClient)


def fetch_file(bucket='blockchain17', key='tmp/eips.csv', region='us-east-1'):
    s3 = boto3.session.Session(region_name=region).client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read()

        
def main():
    regions = get_regions()
    autoscaling_delete_regional(regions)
    add_bastion_regional(regions)
    

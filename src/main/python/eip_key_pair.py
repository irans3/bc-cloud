#!/usr/bin/env python
# Prepare for firewall issues.
import boto3
from ast import literal_eval

# Release redundant addresses to maintain no more than the 5
# permitted elastic IP addresses.
fname = 'regions.json'

with open(fname, 'r') as f:
    regions = literal_eval(f.read())

for key, value in regions.items():
    ec2client = boto3.session.Session(region_name=value).client('ec2')
    # allocation_response = ec2client.allocate_address()
    # print(response['PublicIp'], response['AllocationId'])
    key_name = key + '-dev'
    pem_response = ec2client.create_key_pair(KeyName=key_name)
    with open(key_name + '.pem', 'w') as f:
        f.write(pem_response['KeyMaterial'])

# # Testing
# ec2client.release_address(AllocationId='eipalloc-04c57311e6f82d07a')
# current = ec2client.describe_addresses()
# for i in current['Addresses']:
#     print(i)


for key, value in regions.items():
    ec2client = boto3.session.Session(region_name=key).client('ec2')
    response = ec2client.describe_addresses()
    for i in response['Addresses']:
        print(i)

# Create bastions using AWS quickstart.
{
    'us': 'us-east-1',             # 34.197.105.128
    'tokyo': 'ap-northeast-1',     # 18.179.102.192
    'singapore': 'ap-southeast-1', # 52.221.155.34
    }
for key, value in regions.items():
    key = 'mumbai'
    value = 'ap-south-1'
    # Setup.
    session = boto3.session.Session(region_name=value)
    ec2client = session.client('ec2')
    cf_client = session.client('cloudformation')

    az = ec2client.describe_availability_zones()['AvailabilityZones']
    print(az[0]['ZoneName'], az[1]['ZoneName'])
                    
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
        Tags=[
            {
                'Key': 'Name',
                'Value': key + '-start'
            },
        ]
    )
    print(response['StackId'])


# Attach the EIPs.
for key, value in regions.items():
    # Setup.
    local_session = boto3.session.Session(region_name=value)
    ec2client = local_session.client('ec2')
    ec2client.describe_stacks

local_session = boto3.session.Session(region_name='ap-northeast-2')
ec2client = local_session.client('ec2')
ec2client.describe_addresses()

# Change EIP from 13.209.92.255 to 13.124.188.82.
response = ec2client.associate_address(
        AllocationId='eipalloc-01371523e7ce72428',
        InstanceId='i-0b1bd434440ea2965'
        # PublicIp='string',
        # AllowReassociation=True|False,
        # DryRun=True|False,
        # NetworkInterfaceId='string',
        # PrivateIpAddress='string'
    )


# Instances and regions
regions = {
    'us-east-1' : 'i-05aed69a62906752f',
    'ap-northeast-2' : 'i-0b1bd434440ea2965',
}

    
# Start instances.
for region, instance_id in regions.items():
    ec2client = boto3.session.Session(region_name=region).client('ec2')
    response = ec2client.start_instances(InstanceIds=[instance_id])
    print(response['StartingInstances'][0]['CurrentState'])


# Stop instances.
for region, instance_id in regions.items():
    ec2client = boto3.session.Session(region_name=region).client('ec2')
    response = ec2client.stop_instances(InstanceIds=[instance_id])
    print(response['StoppingInstances'][0]['CurrentState'])

# Update security groups.
my_ip = '147.81.1.10/32'
response = ec2client.authorize_security_group_ingress(
    CidrIp=my_ip
    FromPort=22,
    ToPort=22,
    GroupId='sg-05664237c8943d5b1',
    IpProtocol='TCP'
    )

my_ip = '147.81.1.10/32'
response = ec2client.authorize_security_group_ingress(
    CidrIp=my_ip
    FromPort=22,
    ToPort=22,
    GroupId='sg-0d3f38f95419d3367',
    IpProtocol='TCP'
    )

# Describe instances.
reservations = ec2client.describe_instances()['Reservations']
for reservation in reservations:
    instance = reservation['Instances'][0]
    print('\n{}\t{}'.format(instance['Tags'][0]['Value'], instance['InstanceId']))

#!/usr/bin/env python
# Modify and replace a security group to enable ssh to a specific instance.
import boto3
import sys
import requests

def sec_grp_add():
    try:
        my_ip = requests.get('http://ipecho.net/plain').text
        cidr_ip = my_ip + '/32'
    except:
        print('IP address service was unavailable')

    try:
        instance_id = sys.argv[1]
    except:
        print('Instance ID is required')

    try:
        region = sys.argv[2]
    except:
        region = 'us-east-1'


    print('\nIP address is {}\nInstance ID is {}\nRegion is {}'.format(
        my_ip,
        instance_id,
        region
    ))
    
    local_session = boto3.session.Session(region_name=region)
    ec2client = local_session.client('ec2')
    ress = ec2client.describe_instances()['Reservations']
    sg_id = [x['Instances'][0]['SecurityGroups'][0]['GroupId'] for x in ress if x['Instances'][0]['InstanceId'] == instance_id][0]

    response = ec2client.authorize_security_group_ingress(
        CidrIp=cidr_ip,
        FromPort=22,
        ToPort=22,
        GroupId=sg_id,
        IpProtocol='TCP'
    )

    print(response)


def main():
    sec_grp_add()

    
if __name__=='__main__':
    main()

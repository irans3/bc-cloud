#!/usr/bin/env python
# Associate an EIP with an instance in a region.
# Usage:  ./eip_associate.py <allocation-id> <instance-id> [<region>]
def eip_associate(allocation_id=None, instance_id=None, region='us-east-1'):

    import boto3

    local_session = boto3.session.Session(region_name=region)
    ec2client = local_session.client('ec2')

    if allocation_id == None:
        addresses = ec2client.describe_addresses()['Addresses']
        for address in addresses:
            print(address)

    # Work.
    ec2client.associate_address(
        AllocationId=allocation_id,
        InstanceId=instance_id
    )

    
def main():

    import sys
    
    # Setup.
    try:
        allocation_id = sys.argv[1]
    except:
        print('Allocation ID is required')

    try:
        instance_id = sys.argv[2]
    except:
        print('Instance ID is required')

    try:
        region = sys.argv[3]
    except:
        region = 'us-east-1'

    print('\nAllocation ID is {}\nInstance ID is {}\nRegion is {}'.format(
        allocation_id,
        instance_id,
        region
    ))

    response = eip_associate(
        allocation_id,
        instance_id,
        region
    )
    print(response)

if __name__=='__main__':
    main()

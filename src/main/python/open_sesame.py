#!/usr/bin/env python
# Modify and replace a security group to enable ssh the bastions.
# Steps:
#    1. create stacks for bastions
#    2. assign EIPs to bastions
#    3. open security groups for the bastions to ssh traffic
cf = local_session.client('cloudformation')
stack_list = cf.describe_stacks()['Stacks']
for i in stack_list:
    print(i['StackName'])


"""Open Sesame.
Usage:
  open_sesame.py ship new <name>...
  open_sesame.py ship <name> move <x> <y> [--speed=<kn>]
  open_sesame.py ship shoot <x> <y>
  open_sesame.py mine (set|remove) <x> <y> [--moored|--drifting]
  open_sesame.py -h | --help
  open_sesame.py --version
Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
"""

def load_regions(fname='region-eip.json'):
    from ast import literal_eval
    
    with open(fname, 'r') as f:
        return literal_eval(f.read())

def open_sesame(ip_list, region='us-east-1'):
    import requests
    from boto3 import session
    
    try:
        my_ip = requests.get('http://ipecho.net/plain').text
        cidr_ip = my_ip + '/32'
    except:
        print('IP address service was unavailable')


    print('\nConnecting {} with {}'.format(
        my_ip,
        region
    ))

    local_session = session.Session(region_name=region)
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
   from docopt import docopt

   regions = load_regions()
   arguments = docopt(__doc__, version='Open Sesame 0.0')
   print(arguments, regions)
    
if __name__=='__main__':
    main()

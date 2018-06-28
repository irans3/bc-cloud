#!/usr/bin/env python
# Generate the pem files.
import pandas as pd
import boto3


def generate_pem(region_id, region_name):

    ec2client = boto3.session.Session(region_name=region_id).client('ec2')
    key_name = region_name + '-dev'
    pem_response = ec2client.create_key_pair(KeyName=key_name)
    with open(key_name + '.pem', 'w') as f:
        f.write(pem_response['KeyMaterial'])
            

def generate_pem_regional(fname='region-ip.json'):

    df = pd.read_json(fname)

    for i, row in df.iterrows():
        generate_pem(row[2], row[1])


def main():
    generate_pem_regional()

    
if __name__=='__main__':
    main()

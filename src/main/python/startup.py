import os
from bs4 import BeautifulSoup
# http://www.whtop.com/top.10-alexa-ranking/country-kr
fname = os.path.expanduser('/mnt/c/users/user/Downloads/Korea Top 10 Webhosting companies. Best providers in KR.html')
with open(fname, 'r') as g:
    html_string = g.read()

soup = BeautifulSoup(html_string, 'html5lib')
        

import boto3
import json
ec2client = boto3.client('ec2')
fname = 'regions.json'
txt = ''
with open(fname, 'r') as f:
    d = literal_eval(f.read())

print(d.keys())
    
ec2client.describe_instances()

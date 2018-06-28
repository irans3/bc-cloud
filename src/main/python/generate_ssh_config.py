#!/usr/bin/env python
# Generate the ~/.ssh/config file.
import pandas as pd
import os

def generate_ssh_config(fname='region-ip.json'):

    df = pd.read_json(fname)

    with open(os.path.expanduser('~/.ssh/config'), 'a') as f:
        for i, row in df.iterrows():
            f.write('host {}\n\tHostName {}\n\tUser ubuntu\n\tPort 22\n\tForwardX11 yes\n\tIdentityFile ~/certs/{}-dev.pem\n\n'.format(row[0], row[1], row[0]))

            
def main():
    generate_ssh_config()

    
if __name__=='__main__':
    main()

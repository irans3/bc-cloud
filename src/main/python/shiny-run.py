#!/usr/bin/env python
# Run a container via Fargate.
# 
# Usage:  ./shiny-run.py <region>
def shiny_run(session, repo='terraced'):

    # Setup
    ecs = session.client('ecs')
    ecr = session.client('ecr')
    repository_uri = ecr.describe_repositories()['repositories'][0]['repositoryUri'] + ':latest'
    cluster_response = ecs.register_task_definition(
        family='trust',
        networkMode='awsvpc',
        containerDefinitions=[
            {
                'name': 'trust', #repository_uri + '/ss-shiny-devel:latest',
                'image': repository_uri,
                'memory': 128
            }
        ]
    )

    taskDefinitionArn = cluster_response['taskDefinition']['taskDefinitionArn']
    
    task_response = ecs.run_task(
        cluster=res['cluster']['clusterArn'],
        taskDefinition=taskDefinitionArn,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-717adc18',
                ],
                'securityGroups': [
                    'sg-03608b01e272d7bb2',
                ],
                'assignPublicIp': 'ENABLED'
            }
        }
    )
    

def main():

    from boto3 import session

    try:
        image = sys.argv[1]
    except:
        print('An image ID is required.')
        
    try:
        region = sys.argv[2]
    except:
        try:
            from requests import get
            requests.get('http://169.254.169.254/latest/meta-data/hostname').text.split('.')[1]
        except:
            region = 'ap-south-1'

    local_session = session.Session(region_name=region)
    shiny_run(local_session)
    
    
if __name__=='__main__':
    main()

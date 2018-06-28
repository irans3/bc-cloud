#!/usr/bin/env python
# Transfer project from one region to another.
# Usage: ./region-transfer.py <old-region> <new-region>
from boto3 import session

# Tear down the old region's resources.
def take_down(region):

    local_session = session.Session(region_name=region)

    # ECService
    ecs = local_session.client('ecs')
    delete_ecs(ecs)
        
    # ECRegistry
    ecr = local_session.client('ecr')
    delete_all_repositories(ecr)

    # EC2
    ec2 = local_session.client('ec2')
    shutdown_all_instances(ec2)


def delete_ecs(ecsClient):
    # clusters
    res = ecs.list_clusters()['clusterArns']
    for cluster in res:
        ecs.delete_cluster(cluster=cluster)
        
    # container instances
    res = ecs.list_container_instances()['containerInstanceArns']
    for container in res:
        ecs.deregister_container_instance(containerInstance=container)

    # services
    res = ecs.list_services()['serviceArns']
    for service in res:
        ecs.delete_service(service=service)

    # task definitions
    res = ecs.list_task_definitions()['taskDefinitionArns']
    for taskDefinition in res:
        ecs.deregister_task_definition(
            taskDefinition=taskDefinition
        )

    # tasks
    res = ecs.list_tasks()['taskArns']
    for task in res:
        ecs.stop_task(task=task)

    
def delete_all_repositories(ecrClient):

    res = ecrClient.describe_repositories()['repositories']
    for repo in res:
        images = ecrClient.list_images(repositoryName=repo['repositoryName'])['imageIds']
        ecrClient.batch_delete_image(repositoryName=repo['repositoryName'], imageIds=images)
        ecrClient.delete_repository(repositoryName=repo['repositoryName'])
    
            
def shutdown_all_instances(ec2client):

    reservations = ec2client.describe_instances()['Reservations']
    for reservation in reservations:
        for instance in reservation['Instances']:
            res = ec2client.stop_instances(
                InstanceIds=[instance['InstanceId']])
            print(res)


def terminate_all_instances(ec2client):

    reservations = ec2client.describe_instances()['Reservations']
    for reservation in reservations:
        for instance in reservation['Instances']:
            res = ec2client.terminate_instances(
                InstanceIds=[instance['InstanceId']])
            print(res)

            
def rebuild(region):
    
    local_session = session.Session(region_name=region)

    # EC2
    ec2 = local_session.client('ec2')
    
    
def main():

    import sys

    try:
        old_region = sys.argv[1]
    except:
        old_region = 'ap-south-1'
    try:
        new_region = sys.argv[2]
    except:
        new_region = 'us-east-1'

    take_down(old_region)
    rebuild(new_region)
    
    
if __name__=='__main__':
    main()

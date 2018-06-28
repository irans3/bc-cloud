#!/usr/bin/env python
# Upload a docker image to ECR.
import boto3
import docker

ecr_client = boto3.client('ecr', 'ap-south-1')
docker_client = docker.from_env()

#docker_client.login(
#containers = docker_client.containers
# docker build -t ss-shiny-devel docker/
response = docker_client.images.build(
    path=os.path.expanduser('~/shiny-examples/docker'),
    tag='ss-shiny-devel'
    )

image = docker_client.images.pull('irans3/bc-cloud:latest')

for line in cli.push('yourname/app', stream=True):
    print(line)

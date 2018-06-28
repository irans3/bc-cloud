#!/usr/bin/env python
# Push a docker image to the Elastic Container Registry (ECR).
# Docker commands seem to require sudo.
# Usage:  ./ecr-upload.py <image-id> <region>
def ecr_upload(
        ecrClient, \
        image_id='ss-shiny-devel', \
        src_path='~/shiny-examples/docker', \
        repo_name='terraced'):

    import docker

    try:
        repos = ecrClient.describe_repositories()['repositories']
        registry_id, repo_tag = [[r['registryId'], r['repositoryUri']] for r in repos if r['repositoryName'] == repo_name][0]
    except:
        ecrClient.create_repository(repositoryName=repo_name)
        repos = ecrClient.describe_repositories()['repositories']
        registry_id, repo_tag = [[r['registryId'], r['repositoryUri']] for r in repos if r['repositoryName'] == repo_name][0]

    docker_client = docker.from_env()

    try:
        image = docker_client.images.get(image_id)
    except:
        # docker build -t ss-shiny-devel docker/
        response = docker_client.images.build(
            path=os.path.expanduser(src_path),
            tag=image_id.split(':')[0]
        )
        image = docker_client.images.get(image_id)

    image.tag(repo_tag)

    # docker authorization
    from base64 import b64decode

    auth = ecrClient.get_authorization_token(
            registryIds=[registry_id]
        )['authorizationData'][0]
    token = auth['authorizationToken'].encode()
    user, password = [s.decode() for s in b64decode(token).split(b':')]
    #login_response = docker_client.login(user, password, registry=auth['proxyEndpoint'])

    # Takes time
    for line in docker_client.images.push(
            repository=repo_tag,
            auth_config={
                'username': user,
                'password': password
            },
            stream=True
    ):
        print(line)
    

def my_region():
    from requests import get
    requests.get('http://169.254.169.254/latest/meta-data/hostname').text.split('.')[1]

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
            region = my_region()
        except:
            region = 'ap-south-1'

    local_session = session.Session(region_name=region)
    ecrClient = local_session.client('ecr')
    ecr_upload(ecrClient, image)
    
    
if __name__=='__main__':
    main()

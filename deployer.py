#!/usr/bin/env python3

import argparse
from zipfile import ZipFile

import boto3

REGION = 'us-east-1'
APPLICATION = 'wichita'
STGPREFIX = 'lirio-staging'
BUCKET = 'deploy-052763798005'
VERSION = None

def staging_environment():
    '''Find the environment running in Elastic Beantstalk application with
    name APPLICATION with the CNAME that matches our Staging URL.
    '''

    client = boto3.client('elasticbeanstalk', region_name=REGION)
    response = client.describe_environments(ApplicationName=APPLICATION)
    for environment in response['Environments']:
        if STGPREFIX in environment['CNAME']:
            return environment['EnvironmentName']
    return None

def deploy_to_staging():
    version = VERSION

    with open('/var/tmp/Dockerrun.aws.json', 'w') as myfile:
        dockerrun = '''{
 "AWSEBDockerrunVersion": "1",
 "Image": {
    "Name": "052763798005.dkr.ecr.us-east-1.amazonaws.com/wichita-ecr-andy-docker-app:''' + version + '''",
    "Update": "true"
  },
 "Ports": [
   {
     "ContainerPort": "8080"
   }
 ],
 "Logging": "/var/log"
}
'''
        myfile.write(dockerrun)

    with ZipFile('/var/tmp/dockerapp-{}.zip'.format(version), 'w') as myzip:
        myzip.write('/var/tmp/Dockerrun.aws.json',
                    arcname='Dockerrun.aws.json'
        )

    s3 = boto3.resource('s3', region_name=REGION)
    s3.meta.client.upload_file('/var/tmp/Dockerrun.aws.json',
                               BUCKET,
                               'eb/dockerapp-{}.zip'.format(version))

    client = boto3.client('elasticbeanstalk', region_name=REGION)
# aws elasticbeanstalk create-application-version --application-name wichita --version-label 0.0.4 --source-bundle S3Bucket=acowell-${ACCTID},S3Key=eb/dockerapp-0.0.4.zip
    ebargs = {
        'ApplicationName': APPLICATION,
        'VersionLabel': '{}'.format(version),
        'Description': 'Test deployment',
        'SourceBundle': {
            'S3Bucket': BUCKET,
            'S3Key': 'eb/dockerapp-{}.zip'.format(version)
        }
    }
    response = client.create_application_version(**ebargs)

    ebargs = {
        'ApplicationName': APPLICATION,
        'EnvironmentName': staging_environment(),
        'VersionLabel': '{}'.format(version)
    }
    response = client.update_environment(**ebargs)

def parse_args():
    global VERSION

    parser = argparse.ArgumentParser(description='Deploy from ECR to Lirio application')
    parser.add_argument('version',
                        type=str,
                        help='Version of Lirio app doccker container to deploy to the Staging environment.')
    args = parser.parse_args()
    VERSION = args.version

if __name__ == '__main__':
    parse_args()

    print(staging_environment())
    print(VERSION)

    deploy_to_staging()

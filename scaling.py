from sys import exit
from argparse import ArgumentParser
from datetime import datetime, timedelta
from operator import itemgetter
from requests import get
from boto3.session import Session
import boto3

parser = ArgumentParser(description='EC2 load checker')
parser.add_argument(
    '-w', action='store', dest='warn_threshold', type=float, default=0.65)
parser.add_argument(
    '-c', action='store', dest='crit_threshold', type=float, default=0.95)
arguments = parser.parse_args()

session = Session(
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_KEY',
    region_name='us-east-1')
cw = session.client('cloudwatch')

ec2=boto3.client('ec2')
instance_id=c2.describe_instances(InstanceIds=[{your_InstanceID_in_quotes}])['Reservations'][0]['Instances'][0]['PublicDnsName']
print(instance_id)
now = datetime.utcnow()
past = now - timedelta(minutes=30)
future = now + timedelta(minutes=10)


results = cw.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
    StartTime=past,
    EndTime=future,
    Period=300,
    Statistics=['Average'])

datapoints = results['Datapoints']
last_datapoint = sorted(datapoints, key=itemgetter('Timestamp'))[-1]
utilization = last_datapoint['Average']
load = round((utilization/100.0), 2)
timestamp = str(last_datapoint['Timestamp'])
print("{0} load at {1}".format(load, timestamp))

if load < arguments.warn_threshold:
    exit(0)
elif load > arguments.crit_threshold:
    client = boto3.client('ec2', region_name='us-east-1')

    response = client.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/ritam/xdva',
                'Ebs': {

                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                },
            },
        ],
        ImageId='ami-e3f432f5',
        InstanceType='t3.small',
        MaxCount=1,
        MinCount=1,
        Monitoring={
            'Enabled': True
        },
        SecurityGroupIds=[
            'sg-1f39854x',
        ],
    )



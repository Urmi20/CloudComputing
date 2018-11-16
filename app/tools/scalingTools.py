import boto3
from datetime import datetime, timedelta


class ScalingTool:
    @staticmethod
    def get_instances_load():
        client = boto3.client('cloudwatch')
        ec2 = boto3.resource('ec2')
        # instances = ec2.instances.all()
        metric_name = 'CPUUtilization'
        namespace = 'AWS/EC2'
        statistic = 'Average'
        cpu_metrics = []

        instances = ScalingTool.get_instances_in_load_balancer()

        for instance in instances:
            cpus = client.get_metric_statistics(Period=1 * 60,
                                                StartTime=datetime.utcnow() - timedelta(seconds=1 * 60),
                                                EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
                                                MetricName=metric_name,
                                                Namespace=namespace,
                                                Unit='Percent',
                                                Statistics=[statistic],
                                                Dimensions=[
                                                    {'Name': 'InstanceId', 'Value': instance.get('InstanceId')}])

            metric_read = False
            for cpu in cpus['Datapoints']:
                metric_read = True
                if 'Average' in cpu:
                    cpu_metrics.append((instance.get('InstanceId'), cpu['Average']))
                else:
                    # Instance not running
                    cpu_metrics.append(instance.get('InstanceId'), 0)

            if not metric_read:
                # No metrics found for a given id.
                # Probably cloud watch failed to return.
                cpu_metrics.append((instance.get('InstanceId'), 0))

        return cpu_metrics

    @staticmethod
    def spaw_one_instace():
        client = boto3.client('ec2', region_name='us-east-1')

        response = client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'VirtualName': 'Banana',
                    'Ebs': {

                        'DeleteOnTermination': True,
                        'VolumeSize': 8,
                        'VolumeType': 'standard'
                    },
                },
            ],
            ImageId='ami-05ce302e08cc9baa3',
            InstanceType='t3.small',
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': True
            },
            NetworkInterfaces=[
                {
                    'Groups': [
                        'sg-03e9dfa1729c8ae8a',
                    ],
                    'SubnetId': 'subnet-bc7df692',
                    'DeviceIndex': 0
                }
            ],
            KeyName="Ritam_ECE1779"
        )

        client2 = boto3.client('elb')

        response2 = client2.register_instances_with_load_balancer(
            LoadBalancerName='InstaKilo',
            Instances=[
                {
                    'InstanceId': ''.join([user['InstanceId'] for user in response['Instances']])
                },
            ]
        )

    @staticmethod
    def terminate_one_instance():
        instances = ScalingTool.get_instances_in_load_balancer()
        running_instances_total = len(instances)

        if running_instances_total > 1:
            label, selected_instance = instances[3].popitem()
            ec2 = boto3.resource('ec2')
            ec2.instances.filter(InstanceIds=[selected_instance]).terminate()

    @staticmethod
    def get_instances_in_load_balancer():
        client = boto3.client('elb')
        response = client.describe_load_balancers()
        instances = [user['Instances'] for user in response['LoadBalancerDescriptions']][0]
        return instances

    @staticmethod
    def get_number_of_instances_in_load_balancer():
        instances = ScalingTool.get_instances_in_load_balancer()
        return len(instances)

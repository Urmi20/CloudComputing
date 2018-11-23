import boto3
import time
from datetime import datetime, timedelta
from operator import itemgetter


class ScalingTool:
    @staticmethod
    def get_instances_load(window=60):
        client = boto3.client('cloudwatch')
        ec2 = boto3.resource('ec2')
        # instances = ec2.instances.all()
        metric_name = 'CPUUtilization'
        namespace = 'AWS/EC2'
        statistic = 'Average'
        cpu_metrics = []

        instances = ScalingTool.get_instances_in_load_balancer()
        cpu_stats = []
        for instance in instances:
            cpus = client.get_metric_statistics(Period=1 * 60,
                                                StartTime=datetime.utcnow() - timedelta(seconds=window * 60),
                                                EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
                                                MetricName=metric_name,
                                                Namespace=namespace,
                                                #Unit='Percent',
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


            plot_data = []
            for point in cpus['Datapoints']:
                hour = point['Timestamp'].hour
                minute = point['Timestamp'].minute
                time = hour + minute / 60
                plot_data.append([time, point['Average']])

            plot_data = sorted(plot_data, key=itemgetter(0))
            cpu_stats.append(plot_data)

        return cpu_stats, instances, cpu_metrics

    @staticmethod
    def get_load_balancer_instances_avg_load():
        # This methos assumes the number of instances is never zero
        _a, _b, individual_loads = ScalingTool.get_instances_load(1)
        total_load = 0
        instances = 0
        for load in individual_loads:
            total_load = total_load + load[1]
            instances = instances + 1

        return total_load/instances


    @staticmethod
    def spawn_one_instance():
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
            ImageId='ami-0e3c7d31edc077e74',
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

        time.sleep(5)

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
    def spawn_n_instances(n):
        print('Creating {} instances'.format(n))
        for i in range(int(n)):
            ScalingTool.spawn_one_instance()

    @staticmethod
    def terminate_one_instance(i=1):
        instances = ScalingTool.get_instances_in_load_balancer()
        running_instances_total = len(instances)

        if running_instances_total > i:
            selected_instances = []
            n = 0
            while n < i:
                label, selected_instance = instances[n].popitem()
                selected_instances.append(selected_instance)
                n += 1
            ec2 = boto3.resource('ec2')
            ec2.instances.filter(InstanceIds=selected_instances).terminate()

    @staticmethod
    def terminate_n_instances(n):
        if n != 0:
            print('Terminating {} instances'.format(n))
            ScalingTool.terminate_one_instance(n)

    @staticmethod
    def get_instances_in_load_balancer():
        client = boto3.client('elb')
        response = client.describe_load_balancers()
        instances = [user['Instances'] for user in response['LoadBalancerDescriptions']][0]
        return instances

    @staticmethod
    def get_number_of_in_service_instances_in_load_balancer():
        # instances = ScalingTool.get_instances_in_load_balancer()

        client = boto3.client('elb')
        response = client.describe_instance_health(LoadBalancerName='InstaKilo').get('InstanceStates')
        n_instances = 0

        for instance in response:
            state = instance.get('State')
            if state == 'InService':
                n_instances += 1

        return n_instances

    @staticmethod
    def wait_for_instances_to_settle(expected_number_of_instances):
        print('Waiting for instances to settle in load balancer')
        instances_settled = False
        wait_start_time = datetime.now()

        while not instances_settled:
            time.sleep(10)

            if expected_number_of_instances == ScalingTool.get_number_of_in_service_instances_in_load_balancer():
                print('Instances settled')
                instances_settled = True

            elapsed_time = datetime.now() - wait_start_time

            if elapsed_time > timedelta(minutes=2):
                print('Timeout while waiting for instances to settle')
                instances_settled = True



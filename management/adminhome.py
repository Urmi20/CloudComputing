from flask import render_template, session, redirect, url_for, request
import boto3
from app.tools.fileTools import FileManager
from app.tools.dbTools import DataBaseManager
from datetime import datetime, timedelta
from management import managerUI


@managerUI.route('/admin_main_landing')
def admin_main_landing():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        client = boto3.client('cloudwatch')
        ec2 = boto3.resource('ec2')
        instances = ec2.instances.all()
        metric_name = 'CPUUtilization'
        namespace = 'AWS/EC2'
        statistic = 'Average'
        cpu_metrics = []

        for instance in instances:
            cpus = client.get_metric_statistics(Period=1 * 60,
                                                StartTime=datetime.utcnow() - timedelta(seconds=1 * 60),
                                                EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
                                                MetricName=metric_name,
                                                Namespace=namespace,
                                                Unit='Percent',
                                                Statistics=[statistic],
                                                Dimensions=[{'Name': 'InstanceId', 'Value': instance.id}])

            metric_read = False
            for cpu in cpus['Datapoints']:
                metric_read = True
                if 'Average' in cpu:
                    cpu_metrics.append((instance.id, cpu['Average']))
                else:
                    # Instance not running
                    cpu_metrics.append(instance.id, 0)

            if not metric_read:
                # No metrics found for a given id.
                # Probably cloud watch failed to return.
                cpu_metrics.append((instance.id, 0))

        return render_template('adminhome.html', cpu_metrics=cpu_metrics)

    return redirect(url_for('index'))


@managerUI.route('/delete_all', methods=['POST'])
def delete_all():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        f_mgr = FileManager()
        f_mgr.delete_all_from_s3_bucket()
        dbm = DataBaseManager()
        dbm.reset_database()

        return redirect(url_for('admin_main_landing'))


@managerUI.route('/size_scaling', methods=['POST'])
def size_scaling():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        scale_up_load = request.form.get('uth')
        scale_down_load = request.form.get('dth')
        expand_ratio = request.form.get('ex_ratio')
        shrink_ratio = request.form.get('s_ratio')
        scale_mode = 'automatic'

        dbm = DataBaseManager()
        dbm.scaling(scale_up_load, scale_down_load, expand_ratio, shrink_ratio, scale_mode)

        return redirect(url_for('admin_main_landing'))


@managerUI.route('/add_worker', methods=['POST'])
def add_worker():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
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

        print(response)
        print([user['InstanceId'] for user in response['Instances']])

        client2 = boto3.client('elb')

        response2 = client2.register_instances_with_load_balancer(
            LoadBalancerName='InstaKilo',
            Instances=[
                {
                    'InstanceId': ''.join([user['InstanceId'] for user in response['Instances']])
                },
            ]
        )

        return redirect(url_for('admin_main_landing'))


@managerUI.route('/sub_worker', methods=['POST'])
def sub_worker():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        client = boto3.client('elb')

        response = client.describe_load_balancers()

        print([user['Instances'] for user in response['LoadBalancerDescriptions']])

        return redirect(url_for('admin_main_landing'))

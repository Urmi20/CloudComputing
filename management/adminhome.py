from flask import render_template, session, redirect, url_for
import boto3
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
        cpu_avg = []

        for instance in instances:
            cpus = client.get_metric_statistics(Period=1*60,
                                                StartTime=datetime.utcnow()-timedelta(seconds=5*60),
                                                EndTime=datetime.utcnow()-timedelta(seconds=0*60),
                                                MetricName=metric_name,
                                                Namespace=namespace,
                                                Unit='Percent',
                                                Statistics=[statistic],
                                                Dimensions=[{'Name': 'InstanceId', 'Value': instance.id}])

            cpu_avg.append(0)
            for cpu in cpus['Datapoints']:
                if 'Average' in cpu:
                    cpu_avg.pop()
                    cpu_avg.append(cpu['Average'])

        return render_template('adminhome', instances=instances, cpu_avg=cpu_avg)

    return redirect(url_for('index'))

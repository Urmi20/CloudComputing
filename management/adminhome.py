from flask import render_template, session, redirect, url_for
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
        cpu_metrics=[]

        for instance in instances:
            cpus = client.get_metric_statistics(Period=1*60,
                                                StartTime=datetime.utcnow()-timedelta(seconds=1*60),
                                                EndTime=datetime.utcnow()-timedelta(seconds=0*60),
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


@managerUI.route('/delete_all')
def delete_all():
    f_mgr = FileManager()
    f_mgr.delete_all_from_s3_bucket()

    dbm = DataBaseManager()
    dbm.reset_database()

    return redirect(url_for('admin_main_landing'))


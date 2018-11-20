from flask import render_template, session, redirect, url_for, request
from app.tools.fileTools import FileManager
from app.tools.dbTools import DataBaseManager
from management import managerUI
from app.tools.scalingTools import ScalingTool


@managerUI.route('/admin_main_landing')
def admin_main_landing():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        cpu_stats, instances, _x = ScalingTool.get_instances_load()
        instance_list = [dict['InstanceId'] for dict in instances]
        length = len(cpu_stats)
        dbm = DataBaseManager()
        uth, dth, ex_ratio, s_ratio, mode = dbm.get_scaling_settings()
        return render_template('adminhome.html', length=length, instance_list=instance_list, cpu_stats=cpu_stats, ex_ratio=ex_ratio,
                               s_ratio=s_ratio, uth=uth, dth=dth, mode=mode)

    return redirect(url_for('index'))


@managerUI.route('/delete_all', methods=['POST'])
def delete_all():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        f_mgr = FileManager()
        f_mgr.delete_all_from_s3_bucket()
        dbm = DataBaseManager()
        dbm.reset_database()

        return redirect(url_for('admin_main_landing'))

    return redirect(url_for('index'))


@managerUI.route('/size_scaling', methods=['POST'])
def size_scaling():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        scale_up_load = request.form.get('uth')
        scale_down_load = request.form.get('dth')
        expand_ratio = request.form.get('ex_ratio')
        shrink_ratio = request.form.get('s_ratio')
        scale_mode = 'auto'

        err_msg=[]
        dbm = DataBaseManager()
        cpu_metrics = ScalingTool.get_instances_load()

        if scale_up_load == "" or scale_down_load == "" or expand_ratio == "" or shrink_ratio == "":
            msg = "Fields cannot be empty"
            err_msg.append(msg)
            return render_template('adminhome.html', cpu_metrics=cpu_metrics, err_msg=err_msg,
                                   uth=scale_up_load, dth=scale_down_load, ex_ratio=expand_ratio, s_ratio=shrink_ratio)

        else:

            if float(scale_up_load) < 0:
                msg='Scale Up Load Should be Greater than 0'
                err_msg.append(msg)

            if float(scale_down_load) < 0:
                msg='Scale Down Load Should be Greater than 0'
                err_msg.append(msg)

            if float(scale_up_load) < float(scale_down_load):
                msg='Scale Up Load should be Greater than Scale Down Load'
                err_msg.append(msg)

            if float(expand_ratio) <= 1:
                msg='Expand Ratio should be Greater than 1'
                err_msg.append(msg)

            if float(shrink_ratio) <= 1:
                msg='Shrink Ratio should be Greater than 1'
                err_msg.append(msg)

            if not err_msg:
                dbm.scaling(scale_up_load, scale_down_load, expand_ratio, shrink_ratio, scale_mode)

                return redirect(url_for('admin_main_landing'))

        return render_template('adminhome.html', cpu_metrics=cpu_metrics, error=err_msg,
                               uth=scale_up_load, dth=scale_down_load, ex_ratio=expand_ratio, s_ratio=shrink_ratio)

    return redirect(url_for('index'))


@managerUI.route('/add_worker', methods=['POST'])
def add_worker():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        ScalingTool.spawn_one_instance()
        dbm = DataBaseManager()
        uth, dth, ex_ratio, s_ratio, mode = dbm.get_scaling_settings()
        mode = 'manual'
        dbm.scaling(str(int(uth)), str(int(dth)), str(int(ex_ratio)), str(int(s_ratio)), mode)
        return redirect(url_for('admin_main_landing'))

    return redirect(url_for('index'))



@managerUI.route('/sub_worker', methods=['POST'])
def sub_worker():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        ScalingTool.terminate_one_instance()
        dbm = DataBaseManager()
        uth, dth, ex_ratio, s_ratio, mode = dbm.get_scaling_settings()
        mode = 'manual'
        dbm.scaling(str(int(uth)), str(int(dth)), str(int(ex_ratio)), str(int(s_ratio)), mode)

        return redirect(url_for('admin_main_landing'))

    return redirect(url_for('index'))

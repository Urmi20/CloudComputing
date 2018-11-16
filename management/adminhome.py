from flask import render_template, session, redirect, url_for, request
from app.tools.fileTools import FileManager
from app.tools.dbTools import DataBaseManager
from management import managerUI
from app.tools.scalingTools import ScalingTool


@managerUI.route('/admin_main_landing')
def admin_main_landing():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        cpu_metrics = ScalingTool.get_instances_load()
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

    return redirect(url_for('index'))


@managerUI.route('/size_scaling', methods=['POST'])
def size_scaling():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        scale_up_load = request.form.get('uth')
        scale_down_load = request.form.get('dth')
        expand_ratio = request.form.get('ex_ratio')
        shrink_ratio = request.form.get('s_ratio')
        scale_mode = 'automatic'


        if(scale_up_load>0):
            if(scale_down_load>0):
                if(scale_up_load>scale_down_load):
                    if(expand_ratio>1):
                        if(shrink_ratio>1):

                            dbm = DataBaseManager()
                            dbm.scaling(scale_up_load, scale_down_load, expand_ratio, shrink_ratio, scale_mode)

                            return redirect(url_for('admin_main_landing'))
                        else:
                            msg='Shrink Ratio should be Greater than 1'
                            return render_template("adminhome.html", error=msg, uth=scale_up_load,
                                                   dth=scale_down_load, ex_ratio=expand_ratio, s_ratio=shrink_ratio)
                    else:
                        msg='Expand Ratio should be Greater than 1'
                        return render_template("adminhome.html", error=msg, uth=scale_up_load,
                                               dth=scale_down_load, ex_ratio=expand_ratio, s_ratio=shrink_ratio)

                else:
                    msg='Scale Up Load should be Greater than Scale Down Load'
                    return render_template("adminhome.html", error=msg, uth=scale_up_load,
                                           dth=scale_down_load, ex_ratio=expand_ratio, s_ratio=shrink_ratio)
            else:
                msg='Scale Down Load Should be Greater than 0'
                return render_template("adminhome.html", error=msg, uth=scale_up_load,
                                       dth=scale_down_load, ex_ratio=expand_ratio, s_ratio=shrink_ratio)
        else:
            msg='Scale Up Load Should be Greater than 0'
            return render_template("adminhome.html", error=msg, uth=scale_up_load,
                                    dth=scale_down_load, ex_ratio=expand_ratio, s_ratio=shrink_ratio)

    return redirect(url_for('index'))


@managerUI.route('/add_worker', methods=['POST'])
def add_worker():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        ScalingTool.spaw_one_instace()
        return redirect(url_for('admin_main_landing'))

    return redirect(url_for('index'))



@managerUI.route('/sub_worker', methods=['POST'])
def sub_worker():
    if 'authorized' in session and session['authorized'] is True and 'type' in session and session['type'] == 'admin':
        ScalingTool.terminate_one_instance()

        return redirect(url_for('admin_main_landing'))

    return redirect(url_for('index'))

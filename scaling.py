import time

import boto3
from app.tools.scalingTools import ScalingTool
from app.tools.dbTools import DataBaseManager

while True:
    #time.sleep(10)
    # Get database scaling settings
    dbm = DataBaseManager(False)
    scaling_settings = dbm.get_scaling_settings()
    up_scale_factor = scaling_settings[0][1]
    down_scale_factor = scaling_settings[0][2]
    instance_start_load = scaling_settings[0][3]
    instance_termination_load = scaling_settings[0][4]

    # Get number of instances on load balancer
    total_running_instances = ScalingTool.get_number_of_instances_in_load_balancer()
    #read load balancer average instance loads
    avg_load = 0

    if avg_load < instance_termination_load:
        #terminate one instance
        print('condition')

    if avg_load > instance_start_load:
        n_instances = total_running_instances * up_scale_factor - total_running_instances

import time
from app.tools.scalingTools import ScalingTool
from app.tools.dbTools import DataBaseManager

while True:
    time.sleep(10)
    # Get database scaling settings
    dbm = DataBaseManager(False)
    up_scale_factor, down_scale_factor, instance_start_load, instance_termination_load, mode = dbm.get_scaling_settings()

    if mode != 'automatic':
        continue

    # Get number of instances in service on load balancer
    total_running_instances = ScalingTool.get_number_of_in_service_instances_in_load_balancer()

    # Read load balancer average instance loads
    avg_load = ScalingTool.get_load_balancer_instances_avg_load()

    # Should instances be terminated?
    if avg_load < instance_termination_load:
        n_instances_to_terminate = total_running_instances - total_running_instances // down_scale_factor
        expected_n_instances = total_running_instances - n_instances_to_terminate

        if expected_n_instances <= 1:
            n_instances_to_terminate = total_running_instances - 1
            expected_n_instances = 1

        ScalingTool.terminate_n_instances(n_instances_to_terminate)
        ScalingTool.wait_for_instances_to_settle(expected_n_instances)

    # Should instances be started?
    if avg_load > instance_start_load:
        n_instances_to_start = total_running_instances * up_scale_factor - total_running_instances
        expected_n_instances = total_running_instances + n_instances_to_start

        ScalingTool.spawn_n_instances(n_instances_to_start)
        ScalingTool.wait_for_instances_to_settle(expected_n_instances)

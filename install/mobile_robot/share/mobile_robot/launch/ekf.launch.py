from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # EKF Node with use_sim_time parameter set to true
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[
                '/home/thomas/MobileRobot/ws_new/src/mobile_robot/config/ekf.yaml',
                {'use_sim_time': True}  # Ensure the node uses simulated time
            ]
        ),
    ])

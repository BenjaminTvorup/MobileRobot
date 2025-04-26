import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Paths to configuration files
    pkg_share = get_package_share_directory('mobile_robot')  
    nav2_params = os.path.join(pkg_share, 'config', 'nav2_params.yaml')
    ekf_local_config = os.path.join(pkg_share, 'config', 'ekf.yaml')
    navsat_transform_config = os.path.join(pkg_share, 'config', 'navsat_transform.yaml')

    # robot_localization: EKF for local odometry
    ekf_local = Node(
        package='robot_localization',
        executable='ekf_node',  
        name='ekf',
        output='screen',
        parameters=[ekf_local_config, {'use_sim_time': True}],
        remappings=[('/odometry/filtered', '/odometry/filtered')]
    )

    # robot_localization: NavSat Transform for GPS
    navsat_transform = Node(
        package='robot_localization',
        executable='navsat_transform_node',
        name='navsat_transform',
        output='screen',
        parameters=[navsat_transform_config],
        remappings=[
            ('/imu', '/imu/data'),
            ('/gps/fix','/gps/fix'),
            ('/odometry/filtered', '/odometry/filtered'),
            ('/odometry/gps', '/odometry/gps')
        ]
    )

    # Nav2 stack
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'params_file': nav2_params,
            'use_sim_time': 'true'
        }.items()
    )

    # GPS Waypoint Follower
    waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[nav2_params]
    )
    
    nav2_bt_navigator =   Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
    )


    return LaunchDescription([
        ekf_local,
        navsat_transform,
        
        #nav2_bringup,
        #waypoint_follower,
        #nav2_bt_navigator
    ])
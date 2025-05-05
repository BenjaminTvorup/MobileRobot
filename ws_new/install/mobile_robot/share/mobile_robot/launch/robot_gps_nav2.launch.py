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
    map_yaml = os.path.join(pkg_share, 'map', 'empty_map.yaml')


    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': map_yaml}, {'use_sim_time': True}]
    )

    # robot_localization: EKF for local odometry
    ekf_local = Node(
        package='robot_localization',
        executable='ekf_node',  
        name='ekf_node_odom',
        output='screen',
        parameters=[ekf_local_config, {'use_sim_time': True}],
        remappings=[('/odometry/filtered', '/odometry/filtered')]
    )

    # # robot_localization: NavSat Transform for GPS
    # navsat_transform = Node(
    #     package='robot_localization',
    #     executable='navsat_transform_node',
    #     name='navsat_transform',
    #     output='screen',
    #     parameters=[navsat_transform_config],
    #     remappings=[
    #         ('/imu', '/imu/data'),
    #         ('/gps/fix', '/gps/fix'),
    #         ('/odometry/filtered', '/odometry/filtered'),
    #         ('/odometry/gps', '/odometry/gps')
    #     ]
    # )

    # AMCL (Localization)
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[nav2_params, {'use_sim_time': True}]
    )

    # Nav2 Controller Server
    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_params],
        remappings=[('/cmd_vel', '/cmd_vel_nav')]
    )

    # Nav2 Planner Server
    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_params]
    )

    # Nav2 Behavior Tree Navigator
    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_params]
    )

    # GPS Waypoint Follower
    waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[nav2_params]
    )

    # Nav2 Lifecycle Manager to manage all Nav2 nodes
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{'use_sim_time': True}, {'autostart': True}, 
        #            {'node_names': ['controller_server', 'planner_server', 'bt_navigator', 'waypoint_follower', 'amcl', 'map_server']}]
        #             {'node_names': ['controller_server', 'planner_server', 'bt_navigator', 'waypoint_follower']}]
                     {'node_names': ['controller_server','planner_server','bt_navigator', 'waypoint_follower']}]

    )


    return LaunchDescription([
        #ekf_local,  # i already run ekf in another terminal
        #navsat_transform, # i run in another program
        #map_server, i do not have a map
        #amcl,
        controller_server,
        planner_server,
        bt_navigator,
        waypoint_follower,
        lifecycle_manager
    ])

    
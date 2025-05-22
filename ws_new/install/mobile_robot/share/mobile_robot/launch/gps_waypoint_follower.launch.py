

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    # Paths to configuration files
    pkg_share = get_package_share_directory('mobile_robot')
    nav2_params_path = os.path.join(pkg_share, 'config', 'nav2_no_map_params.yaml')
    ekf_local_config = os.path.join(pkg_share, 'config', 'ekf.yaml')
    navsat_transform_config = os.path.join(pkg_share, 'config', 'navsat_transform.yaml')



    # Rewrite nav2 parameters with substitution support 
    configured_params = RewrittenYaml(
        source_file=nav2_params_path,
        root_key='',
        param_rewrites={},
        convert_types=True
    )

    # Include Navigation2
    navigation2_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': configured_params,
            'autostart': autostart
        }.items()
    )


    # Create launch description
    ld = LaunchDescription()

    # Add actions
    ld.add_action(robot_localization_cmd)
    ld.add_action(navigation2_cmd)


    return ld

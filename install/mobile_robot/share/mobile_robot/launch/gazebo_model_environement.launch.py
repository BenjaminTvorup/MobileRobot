import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

from os.path import expanduser
from virtual_maize_field import get_spawner_launch_file


def generate_launch_description():
    robot_xacro_name = 'ackerman_drive_robot'
    package_name = 'mobile_robot'
    model_file_relative_path = 'model/robot.xacro'
    world_file_relative_path = 'model/empty_world.world'
    controller_file_relative_path = 'config/ackermann_controllers.yaml'

    path_model_file = os.path.join(get_package_share_directory(package_name), model_file_relative_path)
    path_world_file = os.path.join(get_package_share_directory(package_name), world_file_relative_path)
    controller_file = os.path.join(get_package_share_directory(package_name), controller_file_relative_path)
    generated_world_file = os.path.join(expanduser("~"), ".ros", "virtual_maize_field", "generated.world")

    robot_description_config = xacro.process_file(path_model_file)
    robot_description = robot_description_config.toxml()

    # Launch Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={
            'gz_args': '-r -v 4 ' + generated_world_file,
            'use_sim_time': 'true',
        }.items()
    )

    # Spawn the robot
    spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', robot_xacro_name, '-topic', 'robot_description', '-x', '0.0', '-y', '0.0', '-z', '0.5'],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
    
    # Robot state publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    # Bridge configuration
    bridge_params = os.path.join(get_package_share_directory(package_name), 'config', 'gz_bridge.yaml')
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}'],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # Spawn controllers

    controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['ackermann_steering_controller', 'joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        parameters=[{'use_sim_time': True}, controller_file],
        output='screen'
    )

    robot_spawner_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(get_spawner_launch_file()),
    launch_arguments={"robot_name": robot_xacro_name}.items()
)
    # Add twist_mux node
    twist_mux_params = os.path.join(get_package_share_directory(package_name), 'config', 'twist_mux.yaml')
    twist_mux = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_mux_params, {'use_sim_time': True}],
        remappings=[('/cmd_vel_out', '/ackermann_steering_controller/cmd_vel')],
        output='screen'
    )

    # Define the launch description
    return LaunchDescription([
        gazebo_launch
        #robot_state_publisher_node
        #bridge_node,
        #controller_spawner,
        
        #robot_spawner_launch,  # Spawns your robot in the generated world
        #twist_mux  # If needed for velocity management
    ])
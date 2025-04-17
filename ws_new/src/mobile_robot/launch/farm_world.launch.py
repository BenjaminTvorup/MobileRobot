import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro
from launch.conditions import UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, TextSubstitution

def generate_launch_description():
    # Package and file definitions
    package_name = 'mobile_robot'
    robot_xacro_name = 'ackerman_drive_robot'
    model_file_relative_path = 'model/robot.xacro'
    controller_file_relative_path = 'config/ackermann_controllers.yaml'
    rviz_config_file_path = 'config/main.rviz'
    farm_world_file = os.path.join(get_package_share_directory(package_name), 'worlds', 'farm_world.sdf')

    # File paths
    path_model_file = os.path.join(get_package_share_directory(package_name), model_file_relative_path)
    controller_file = os.path.join(get_package_share_directory(package_name), controller_file_relative_path)
    rviz_config_file = os.path.join(get_package_share_directory(package_name), rviz_config_file_path)

    # Launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='True',
        description='Flag to enable use_sim_time'
    )

    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='True',
        description='Flag to enable joint_state_publisher_gui'
    )

    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=path_model_file,
        description='Absolute path to robot model file'
    )

    rvizconfig_arg = DeclareLaunchArgument(
        name='rvizconfig',
        default_value=rviz_config_file,
        description='Absolute path to RViz config file'
    )

    world_arg = DeclareLaunchArgument(
        name='world',
        default_value=farm_world_file,
        description='Path to the SDF world file'
    )

    # Process Xacro file
    robot_description_config = xacro.process_file(path_model_file)
    robot_description = robot_description_config.toxml()

    # Launch Gazebo with farm world
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={
            'gz_args': ['-r', '-v', '4', LaunchConfiguration('world')],
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
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                   '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry'],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # Controller manager node
    controller_manager_node = TimerAction(
        period=2.0,
        actions=[
            Node(
                package='controller_manager',
                executable='ros2_control_node',
                parameters=[{'robot_description': robot_description}, controller_file],
                output='screen'
            )
        ]
    )

    # Spawn controllers
    controller_spawner = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['ackermann_steering_controller', 'joint_state_broadcaster', '--controller-manager', '/controller_manager'],
                parameters=[{'use_sim_time': True}, controller_file],
                output='screen'
            )
        ]
    )

    # Joint state publisher
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', LaunchConfiguration('model')]),
            'use_sim_time': True
        }],
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )

    # RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        parameters=[{'use_sim_time': True}]
    )

    # RTK farm navigation node
    rtk_navigation_node = Node(
        package='mobile_robot',
        executable='rtk_farm_navigation',
        name='rtk_farm_navigation',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # Define the launch description
    return LaunchDescription([
        use_sim_time_arg,
        gui_arg,
        model_arg,
        rvizconfig_arg,
        world_arg,
        gazebo_launch,
        spawn_node,
        robot_state_publisher_node,
        bridge_node,
        controller_manager_node,
        controller_spawner,
        joint_state_publisher_node,
        rviz_node,
        rtk_navigation_node
    ])  
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


print("Starting launch file parsing")

def generate_launch_description():
    robot_xacro_name = 'ackerman_drive_robot'
    package_name = 'mobile_robot'
    model_file_relative_path = 'model/robot.xacro'
    world_file_relative_path = 'model/empty_world.world'
    controller_file_relative_path = 'config/ackermann_controllers.yaml'
    rviz_config_file_path = 'config/main.rviz'
    pkg_share = get_package_share_directory('mobile_robot')  
    

    path_model_file = os.path.join(get_package_share_directory(package_name), model_file_relative_path)
    path_world_file = os.path.join(get_package_share_directory(package_name), world_file_relative_path)
    controller_file = os.path.join(get_package_share_directory(package_name), controller_file_relative_path)
    rviz_config_file = os.path.join(get_package_share_directory(package_name),rviz_config_file_path )
    ekf_local_config = os.path.join(pkg_share, 'config', 'ekf.yaml')
    navsat_transform_config = os.path.join(pkg_share, 'config', 'navsat_transform.yaml')


    # These define configurable options that can be passed when running the launch file
    gui_arg = DeclareLaunchArgument(
        name='gui',  # Name of the argument, used as a flag (e.g., ros2 launch ... gui:=false)
        default_value='True',  # Default is True, enabling the GUI by default
        description='Flag to enable joint_state_publisher_gui'  # Explains that this toggles the GUI version of joint state publisher
    )  # This allows switching between GUI and non-GUI joint state publishing for testing/debugging

    model_arg = DeclareLaunchArgument(
        name='model',  # Argument name for specifying the robot model file
        default_value=path_model_file,  # Defaults to your robot.xacro file’s path, ensuring the correct URDF is used
        description='Absolute path to robot model file'  # Indicates this sets the URDF/Xacro file for the robot description
    )  # This makes it easy to change the model file via command line if needed, ensuring flexibility

    rvizconfig_arg = DeclareLaunchArgument(
        name='rvizconfig',  # Argument name for specifying the RViz configuration file
        default_value=os.path.join(get_package_share_directory(package_name), 'rviz', 'config.rviz'),  # Default path to RViz config in your package
        description='Absolute path to RViz config file'  # Describes that this sets up RViz’s display settings
    )  # This allows customization of RViz visualization (e.g., showing TF, odometry) via a config file


    robot_description_config = xacro.process_file(path_model_file)
    robot_description = robot_description_config.toxml()

    

    # Launch Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={
            'gz_args': '-r -v 4 ' + path_world_file,
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
    controller_spawner = TimerAction(
    period=5.0,  # Wait 5 seconds to ensure controller manager is ready
    actions=[
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['--controller-manager', '/controller_manager','ackermann_steering_controller', 'joint_state_broadcaster'],
            parameters=[{'use_sim_time': True}, controller_file],
            output='screen'
        )
    ])



    # Add twist_mux node
    twist_mux_params = os.path.join(get_package_share_directory(package_name), 'config', 'twist_mux.yaml')
    twist_mux = Node(   
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_mux_params, {'use_sim_time': True}],
        remappings=[('/cmd_vel', '/cmd_vel')],
        output='screen'
    )


    # These are ROS 2 nodes added to the launch file to enhance functionality and visualization
    
    joint_state_publisher_node = Node(
        package='joint_state_publisher',  # ROS package providing joint state publishing
        executable='joint_state_publisher',  # The executable that publishes joint states
        name='joint_state_publisher',  # Unique name for this node instance
        parameters=[{  # Parameters passed to the node
            'robot_description': Command(['xacro ', LaunchConfiguration('model')]),  # Generates the robot description by processing the Xacro file
            'use_sim_time': True  # Syncs the node’s time with Gazebo’s simulation clock
        }],
        condition=UnlessCondition(LaunchConfiguration('gui'))  # Only runs if gui=False, avoiding conflict with the GUI version
    )  # Publishes /joint_states for non-actuated joints; useful when Gazebo’s joint_state_broadcaster isn’t enough

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',  # Package providing a GUI for joint state publishing
        executable='joint_state_publisher_gui',  # Executable that launches a GUI to manually control joints
        name='joint_state_publisher_gui',  # Unique name for this node instance
        condition=IfCondition(LaunchConfiguration('gui'),)  # Only runs if gui=True, enabling manual joint control
    )  # Provides a graphical interface to adjust joint positions (e.g., wheels), handy for testing outside simulation control

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],  # Use the launch argument
        parameters=[{'use_sim_time': True}]
    )

    use_sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='True',
        description='Flag to enable use_sim_time'
    )


    # Nav2 lifecycle manager to manage Nav2 nodes
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'autostart': True},
            {'node_names': ['controller_server']}
        ]
    )



    # Node from the package that contains your KinematicsNode
    kinematics_node = Node(
        package='my_kinematics_pkg',
        executable='kinematics_node',
        name='kinematics_node',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )


    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',  
        name='ekf_node_odom',
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
        parameters=[navsat_transform_config, {'use_sim_time': True}],
        remappings=[
            ('/imu', '/imu/data'),
            ('/gps/fix','/gps/fix'),
            ('/odometry/filtered', '/odometry/filtered'),
            ('/odometry/gps', '/odometry/gps')
        ]
    )

    # Define the launch description
    return LaunchDescription([
        use_sim_time_arg,
        gui_arg,
        model_arg,
        rvizconfig_arg,
        gazebo_launch,
        spawn_node,
        controller_spawner,
        robot_state_publisher_node,
        bridge_node,
        joint_state_publisher_node,
        #joint_state_publisher_gui_node,
        #robot_localization_node,
        rviz_node,
        #twist_mux,
        #nav2_controller_node,
        #lifecycle_manage_node
        #kinematics_node,
        ekf_node,
        navsat_transform
    ])  
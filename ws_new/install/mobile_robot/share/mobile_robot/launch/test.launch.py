import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
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

    

    path_model_file = os.path.join(get_package_share_directory(package_name), model_file_relative_path)
    path_world_file = os.path.join(get_package_share_directory(package_name), world_file_relative_path)
    controller_file = os.path.join(get_package_share_directory(package_name), controller_file_relative_path)
    rviz_config_file = os.path.join(get_package_share_directory(package_name),rviz_config_file_path )

    #
    #
    #

    # These define configurable options that can be passed when running the launch file
    gui_arg = DeclareLaunchArgument(
        name='gui',  # Name of the argument, used as a flag (e.g., ros2 launch ... gui:=false)
        default_value='True',  # Default is True, enabling the GUI by default
        description='Flag to enable joint_state_publisher_gui'  # Explains that this toggles the GUI version of joint state publisher
    )  # This allows switching between GUI and non-GUI joint state publishing for testing/debugging
    # Define the launch description



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
    return LaunchDescription([
        gui_arg,
        gazebo_launch,
       # model_arg,
        #rvizconfig_arg

    ])
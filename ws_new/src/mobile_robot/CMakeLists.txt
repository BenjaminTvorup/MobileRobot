cmake_minimum_required(VERSION 3.8)
project(mobile_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ros_gz_sim REQUIRED)         # For Gazebo Harmonic integration
find_package(ros_gz_bridge REQUIRED)      # For bridging ROS 2 and Gazebo
find_package(controller_manager REQUIRED) # For ros2_control manager
find_package(gz_ros2_control REQUIRED)    # For Gazebo Harmonic ros2_control plugin
#find_package(joint_state_publisher REQUIRED)
#find_package(robot_state_publisher REQUIRED)
find_package(xacro REQUIRED)

# Install directories

install(
  DIRECTORY launch model config
  DESTINATION share/${PROJECT_NAME}/
)



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

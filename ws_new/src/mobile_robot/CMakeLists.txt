cmake_minimum_required(VERSION 3.8)
project(mobile_robot)

# Enable warnings
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(ros_gz_sim REQUIRED)
find_package(ros_gz_bridge REQUIRED)
find_package(controller_manager REQUIRED)
find_package(gz_ros2_control REQUIRED)
find_package(xacro REQUIRED)

# Add backward-cpp (assumes it's in libs/backward-cpp relative to workspace root)
add_subdirectory("/home/thomas/backward-cpp/backward-cpp" backward)


# Include directories
include_directories(include)


### Commented out because my_node is missing and i have not created it yet
# Add your C++ executable
# add_executable(my_node src/my_node.cpp)

# # Link dependencies
# ament_target_dependencies(my_node
#   rclcpp
#   std_msgs
#   controller_manager
#   gz_ros2_control
# )

# # Link backward-cpp
# target_link_libraries(my_node backward)


# # Install binary
# install(TARGETS my_node
#   DESTINATION lib/${PROJECT_NAME}
# )

# Install resource files
install(
  DIRECTORY map launch model config description
  DESTINATION share/${PROJECT_NAME}/
)

# Linting
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

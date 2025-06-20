# Install script for directory: /home/thomas/MobileRobot/ws_new/src/navigation2/nav2_dwb_controller/dwb_critics

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/thomas/MobileRobot/ws_new/install/dwb_critics")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdwb_critics.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdwb_critics.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdwb_critics.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/libdwb_critics.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdwb_critics.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdwb_critics.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdwb_critics.so"
         OLD_RPATH "/home/thomas/MobileRobot/ws_new/install/nav2_costmap_2d/lib:/home/thomas/MobileRobot/ws_new/install/nav_2d_msgs/lib:/home/thomas/MobileRobot/ws_new/install/costmap_queue/lib:/home/thomas/MobileRobot/ws_new/install/dwb_core/lib:/home/thomas/MobileRobot/ws_new/install/dwb_msgs/lib:/home/thomas/MobileRobot/ws_new/install/nav2_voxel_grid/lib:/home/thomas/MobileRobot/ws_new/install/visualization_msgs/lib:/home/thomas/MobileRobot/ws_new/install/nav2_behavior_tree/lib:/home/thomas/MobileRobot/ws_new/install/sensor_msgs/lib:/home/thomas/MobileRobot/ws_new/install/std_srvs/lib:/home/thomas/MobileRobot/ws_new/install/nav_2d_utils/lib:/home/thomas/MobileRobot/ws_new/install/geometry_msgs/lib:/home/thomas/MobileRobot/ws_new/install/nav_msgs/lib:/home/thomas/MobileRobot/ws_new/install/std_msgs/lib:/home/thomas/MobileRobot/ws_new/install/nav2_msgs/lib:/home/thomas/MobileRobot/ws_new/install/nav2_util/lib:/opt/ros/jazzy/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdwb_critics.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/" TYPE DIRECTORY FILES "/home/thomas/MobileRobot/ws_new/src/navigation2/nav2_dwb_controller/dwb_critics/include/")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/src/navigation2/nav2_dwb_controller/dwb_critics/default_critics.xml")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/environment" TYPE FILE FILES "/opt/ros/jazzy/lib/python3.12/site-packages/ament_package/template/environment_hook/library_path.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/environment" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_environment_hooks/library_path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/src/navigation2/nav2_dwb_controller/dwb_critics/default_critics.xml")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/package_run_dependencies" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/dwb_critics")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/parent_prefix_path" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/dwb_critics")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/environment" TYPE FILE FILES "/opt/ros/jazzy/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/environment" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_environment_hooks/ament_prefix_path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/environment" TYPE FILE FILES "/opt/ros/jazzy/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/environment" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_environment_hooks/path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_environment_hooks/local_setup.bash")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_environment_hooks/local_setup.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_environment_hooks/local_setup.zsh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_environment_hooks/local_setup.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_environment_hooks/package.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_index/share/ament_index/resource_index/packages/dwb_critics")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/dwb_core__pluginlib__plugin" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_index/share/ament_index/resource_index/dwb_core__pluginlib__plugin/dwb_critics")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/cmake" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_export_include_directories/ament_cmake_export_include_directories-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/cmake" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_export_libraries/ament_cmake_export_libraries-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/cmake" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_export_dependencies/ament_cmake_export_dependencies-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics/cmake" TYPE FILE FILES
    "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_core/dwb_criticsConfig.cmake"
    "/home/thomas/MobileRobot/ws_new/build/dwb_critics/ament_cmake_core/dwb_criticsConfig-version.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dwb_critics" TYPE FILE FILES "/home/thomas/MobileRobot/ws_new/src/navigation2/nav2_dwb_controller/dwb_critics/package.xml")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/thomas/MobileRobot/ws_new/build/dwb_critics/test/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/thomas/MobileRobot/ws_new/build/dwb_critics/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")

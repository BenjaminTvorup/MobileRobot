#!/usr/bin/env python3
# Copyright 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from nav_msgs.msg import Odometry  # Added for odometry subscription
import rclpy
from rclpy.duration import Duration
from rclpy.node import Node  # Added to create a node for subscription

"""
Basic navigation demo to go to poses.
"""

class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')
        self.navigator = BasicNavigator()
        self.current_pose = None
        # Subscribe to /odometry/gps to get the robot's current pose
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odometry/gps',
            self.odom_callback,
            10
        )

    def odom_callback(self, msg):
        """Callback to store the latest odometry pose."""
        self.current_pose = msg.pose.pose
        self.get_logger().info('Received odometry pose')

    def wait_for_odometry(self, timeout_sec=10.0):
        """Wait for odometry data with a timeout."""
        start_time = self.get_clock().now()
        while self.current_pose is None and (self.get_clock().now() - start_time).nanoseconds / 1e9 < timeout_sec:
            self.get_logger().info('Waiting for odometry data from /odometry/gps...')
            rclpy.spin_once(self, timeout_sec=0.1)
        if self.current_pose is None:
            self.get_logger().error('No odometry data received after timeout')
            return False
        return True

def main() -> None:
    rclpy.init()

    # Create a node instance instead of just BasicNavigator
    node = NavigatorNode()

    # Wait for odometry data before setting initial pose
    if not node.wait_for_odometry():
        node.get_logger().error('Failed to get initial pose, shutting down')
        rclpy.shutdown()
        return

    # Set initial pose from odometry data
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'odom'  # Changed to 'odom' since /odometry/gps is likely in this frame
    initial_pose.header.stamp = node.get_clock().now().to_msg()
    initial_pose.pose = node.current_pose  # Use the received odometry pose
    node.navigator.setInitialPose(initial_pose)

    # Wait for navigation to fully activate
    node.navigator.waitUntilNav2Active()

    # Define goal poses (waypoints) - unchanged
    goal_poses = []
    goal_pose1 = PoseStamped()
    goal_pose1.header.frame_id = 'map'
    goal_pose1.header.stamp = node.get_clock().now().to_msg()
    goal_pose1.pose.position.x = 10.15
    goal_pose1.pose.position.y = -0.77
    goal_pose1.pose.orientation.w = 1.0
    goal_pose1.pose.orientation.z = 0.0
    goal_poses.append(goal_pose1)

    goal_pose2 = PoseStamped()
    goal_pose2.header.frame_id = 'map'
    goal_pose2.header.stamp = node.get_clock().now().to_msg()
    goal_pose2.pose.position.x = 17.86
    goal_pose2.pose.position.y = -0.77
    goal_pose2.pose.orientation.w = 1.0
    goal_pose2.pose.orientation.z = 0.0
    goal_poses.append(goal_pose2)

    goal_pose3 = PoseStamped()
    goal_pose3.header.frame_id = 'map'
    goal_pose3.header.stamp = node.get_clock().now().to_msg()
    goal_pose3.pose.position.x = 21.58
    goal_pose3.pose.position.y = -3.5
    goal_pose3.pose.orientation.w = 1.0
    goal_pose3.pose.orientation.z = 0.0
    goal_poses.append(goal_pose3)

    # Follow waypoints - unchanged
    nav_start = node.get_clock().now()
    node.navigator.followWaypoints(goal_poses)

    i = 0
    while not node.navigator.isTaskComplete():
        i = i + 1
        feedback = node.navigator.getFeedback()
        if feedback and i % 5 == 0:
            print(
                'Executing current waypoint: '
                + str(feedback.current_waypoint + 1)
                + '/'
                + str(len(goal_poses))
            )
            now = node.get_clock().now()
            if now - nav_start > Duration(seconds=600.0):
                node.navigator.cancelTask()
            if now - nav_start > Duration(seconds=35.0):
                goal_pose4 = PoseStamped()
                goal_pose4.header.frame_id = 'map'
                goal_pose4.header.stamp = now.to_msg()
                goal_pose4.pose.position.x = 0.0
                goal_pose4.pose.position.y = 0.0
                goal_pose4.pose.orientation.w = 1.0
                goal_pose4.pose.orientation.z = 0.0
                goal_poses = [goal_pose4]
                nav_start = now
                node.navigator.followWaypoints(goal_poses)

    # Handle result - unchanged
    result = node.navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        (error_code, error_msg) = node.navigator.getTaskError()
        print(f'Goal failed! {error_code}: {error_msg}')
    else:
        print('Goal has an invalid return status!')

    node.navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()  
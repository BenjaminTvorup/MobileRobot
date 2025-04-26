#!/usr/bin/env python3
# This is a ROS2 Python node that uses nav2_simple_commander to navigate through a series of waypoints.

from geometry_msgs.msg import PoseStamped  # For defining robot poses
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult  # Navigation helper
from nav_msgs.msg import Odometry  # To receive fused odometry data
import rclpy  # ROS2 Python client library
from rclpy.duration import Duration  # For handling time durations
from rclpy.node import Node  # Base class for creating ROS2 nodes

"""
Basic navigation demo that navigates the robot through a sequence of goal positions.
"""

class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')  # Create a node named 'navigator_node'
        self.navigator = BasicNavigator()  # Initialize the Nav2 Simple Commander
        self.current_pose = None  # Will hold the latest fused pose from localization

        # Subscribe to the fused odometry topic (e.g., robot_localization output)
        # This should be configured to provide a global pose in the 'map' frame
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odometry/filtered',  # Fused pose output by robot_localization
            self.odom_callback,
            10  # QoS depth: queue up to 10 messages
        )

    def odom_callback(self, msg):
        """Callback to store the latest fused odometry pose."""
        self.current_pose = msg.pose.pose  # Save the Pose (position + orientation)
        self.get_logger().info('Received fused odometry pose')

    def wait_for_odometry(self, timeout_sec=10.0):
        """Wait until we receive at least one fused pose message, with timeout."""
        start_time = self.get_clock().now()
        # Spin until current_pose is set or we hit the timeout
        while self.current_pose is None and (self.get_clock().now() - start_time).nanoseconds / 1e9 < timeout_sec:
            self.get_logger().info('Waiting for fused odometry on /odometry/filtered...')
            rclpy.spin_once(self, timeout_sec=0.1)
        if self.current_pose is None:
            self.get_logger().error('No fused odometry received within timeout')
            return False
        return True


def main() -> None:
    rclpy.init()  # Initialize ROS2
    node = NavigatorNode()  # Instantiate our custom navigator node

    # Wait for the first fused odometry message
    if not node.wait_for_odometry():
        node.get_logger().error('Failed to get initial pose, shutting down')
        rclpy.shutdown()
        return

    # Create a PoseStamped message to set the robot's initial pose in Nav2
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'  # Use the global 'map' frame
    initial_pose.header.stamp = node.get_clock().now().to_msg()  # Timestamp now
    initial_pose.pose = node.current_pose  # Use the fused pose from localization

    # Send the initial pose to Nav2
    node.navigator.setInitialPose(initial_pose)

    # Wait until Nav2 is fully active before sending goals
    node.navigator.waitUntilNav2Active()

    # Define a sequence of goal waypoints in the 'map' frame
    goal_poses = []
    for x, y in [(10.15, -0.77), (17.86, -0.77), (21.58, -3.5)]:
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = node.get_clock().now().to_msg()
        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.orientation.w = 1.0
        goal.pose.orientation.z = 0.0
        goal_poses.append(goal)

    # # Begin following the waypoints
    nav_start = node.get_clock().now()
    node.navigator.followWaypoints(goal_poses)


    # i = 0
    # # Monitor progress until the navigation task completes
    # while not node.navigator.isTaskComplete():
    #     i += 1
    #     feedback = node.navigator.getFeedback()
    #     if feedback and i % 5 == 0:
    #         print(f"Executing waypoint {feedback.current_waypoint + 1}/{len(goal_poses)}")
    #         now = node.get_clock().now()

    #         # If it's been over 10 minutes, cancel the task
    #         if now - nav_start > Duration(seconds=600.0):
    #             node.navigator.cancelTask()

    #         # After 35 seconds, redirect to home (0,0)
    #         if now - nav_start > Duration(seconds=35.0):
    #             home = PoseStamped()
    #             home.header.frame_id = 'map'
    #             home.header.stamp = now.to_msg()
    #             home.pose.position.x = 0.0
    #             home.pose.position.y = 0.0
    #             home.pose.orientation.w = 1.0
    #             home.pose.orientation.z = 0.0
    #             node.navigator.followWaypoints([home])
    #             nav_start = now

    # # Check the result of the navigation
    # result = node.navigator.getResult()
    # if result == TaskResult.SUCCEEDED:
    #     print('Goal succeeded!')
    # elif result == TaskResult.CANCELED:
    #     print('Goal was canceled!')
    # elif result == TaskResult.FAILED:
    #     code, msg = node.navigator.getTaskError()
    #     print(f'Goal failed! {code}: {msg}')
    # else:
    #     print('Invalid task result status')

    # # Shutdown Nav2 and ROS2
    # node.navigator.lifecycleShutdown()
    # rclpy.shutdown()

if __name__ == '__main__':
    main()

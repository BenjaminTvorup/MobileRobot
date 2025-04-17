#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateThroughPoses
from robot_localization.srv import FromLL
from geographic_msgs.msg import GeoPoint
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from tf_transformations import quaternion_from_euler, euler_from_quaternion
import numpy as np

class GPSPathFollower(Node):
    def __init__(self):
        super().__init__('gps_path_follower')
        # Service client for converting GPS to map frame (not used in this version)
        self.from_ll_client = self.create_client(FromLL, 'fromLL')  # Kept for compatibility
        while not self.from_ll_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for fromLL service...')
        # Action client for NavigateThroughPoses
        self.action_client = ActionClient(self, NavigateThroughPoses, 'navigate_through_poses')  # EDIT: Adjust if remapped
        # Subscriber for odometry
        self.odom_sub = self.create_subscription(
            Odometry,
            'odemtry/gps',  # Your topic name
            self.odom_callback,
            10)
        self.current_pose = None

    def odom_callback(self, msg):
        """Store the latest odometry pose."""
        self.current_pose = msg.pose.pose

    def convert_gps_to_map(self, lat, lon):
        """Convert GPS coordinates to a PoseStamped in the map frame (kept for compatibility)."""
        geo_point = GeoPoint()
        geo_point.latitude = lat
        geo_point.longitude = lon
        geo_point.altitude = 0.0  # EDIT: Set altitude if relevant
        request = FromLL.Request()
        request.ll_point = geo_point
        future = self.from_ll_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            return future.result().map_point
        else:
            self.get_logger().error(f'Failed to convert GPS ({lat}, {lon}) to map frame')
            return None

    def compute_yaw(self, pose1, pose2):
        """Compute yaw from the direction between two poses."""
        dx = pose2.pose.position.x - pose1.pose.position.x
        dy = pose2.pose.position.y - pose1.pose.position.y
        return np.arctan2(dy, dx)

    def create_pose_stamped(self, original_pose, yaw):
        """Create a PoseStamped with specified yaw."""
        pose = PoseStamped()
        pose.header.frame_id = 'map'  # EDIT: Adjust if your odometry uses a different frame
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position = original_pose.pose.position
        quat = quaternion_from_euler(0, 0, yaw)
        pose.pose.orientation.x = quat[0]
        pose.pose.orientation.y = quat[1]
        pose.pose.orientation.z = quat[2]
        pose.pose.orientation.w = quat[3]
        return pose

    def compute_forward_pose(self, distance=5.0):
        """Compute a waypoint 'distance' meters forward from current pose."""
        if self.current_pose is None:
            self.get_logger().error('No pose available yet')
            return None

        # Extract current position and orientation
        x = self.current_pose.position.x
        y = self.current_pose.position.y
        orientation = self.current_pose.orientation
        # Convert quaternion to yaw
        quaternion = [orientation.x, orientation.y, orientation.z, orientation.w]
        _, _, yaw = euler_from_quaternion(quaternion)

        # Compute new position (move forward along current heading)
        new_x = x + distance * np.cos(yaw)
        new_y = y + distance * np.sin(yaw)

        # Create a PoseStamped for the new waypoint
        forward_pose = PoseStamped()
        forward_pose.header.frame_id = 'map'
        forward_pose.header.stamp = self.get_clock().now().to_msg()
        forward_pose.pose.position.x = new_x
        forward_pose.pose.position.y = new_y
        forward_pose.pose.position.z = 0.0
        forward_pose.pose.orientation = self.current_pose.orientation  # Maintain current orientation

        return forward_pose

    def follow_path(self, map_poses):
        """Send poses to Nav2 (adapted for map-frame poses)."""
        nav_poses = []
        for i in range(len(map_poses) - 1):
            yaw = self.compute_yaw(map_poses[i], map_poses[i + 1])
            pose = self.create_pose_stamped(map_poses[i], yaw)
            nav_poses.append(pose)
        if len(map_poses) > 1:
            last_pose = self.create_pose_stamped(map_poses[-1], yaw)
            nav_poses.append(last_pose)
        elif len(map_poses) == 1:
            pose = self.create_pose_stamped(map_poses[0], 0.0)  # Default yaw
            nav_poses.append(pose)

        goal_msg = NavigateThroughPoses.Goal()
        goal_msg.poses = nav_poses
        self.action_client.wait_for_server()
        self.action_client.send_goal_async(goal_msg)
        self.get_logger().info(f'Sent {len(nav_poses)} poses to NavigateThroughPoses')

def main():
    rclpy.init()
    node = GPSPathFollower()
    
    # Wait for odometry data
    while node.current_pose is None and not rclpy.ok():
        node.get_logger().info('Waiting for odometry data...')
        rclpy.spin_once(node, timeout_sec=1.0)
    
    # Compute a single waypoint 5 meters forward
    forward_pose = node.compute_forward_pose(distance=5.0)  # EDIT: Adjust distance as needed
    if forward_pose is None:
        node.get_logger().error('Failed to compute forward pose, shutting down')
        node.destroy_node()
        rclpy.shutdown()
        return

    # Send the waypoint to Nav2
    node.follow_path([forward_pose])  # Pass as a list for compatibility
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
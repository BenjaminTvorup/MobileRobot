#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
import numpy as np
from tf_transformations import euler_from_quaternion

class RTKFarmNavigation(Node):
    def __init__(self):
        super().__init__('rtk_farm_navigation')
        
        # Publishers
        self.gps_pub = self.create_publisher(NavSatFix, '/rtk_gps', 10)
        self.cmd_pub = self.create_publisher(Twist, '/ackermann_steering_controller/cmd_vel', 10)
        
        # Subscriber for odometry
        self.create_subscription(Odometry, '/odom_my', self.odom_callback, 10)
        
        # Parameters
        self.current_position = None
        self.current_yaw = 0.0
        self.waypoints = []
        self.base_station_pos = (0.0, 0.0)
        self.GPS_NOISE = 0.01  # Standard GPS noise in meters
        self.RTK_PRECISION = 0.02  # RTK-corrected precision in meters
        
        # Generate waypoints
        self.generate_waypoints()
        self.get_logger().info(f"Waypoints generated: {self.waypoints}")
        
        # Timer for control loop
        self.create_timer(0.1, self.control_vehicle)

    def generate_waypoints(self):
        """Generate a simple set of waypoints along crop rows."""
        self.waypoints = [(float(x), 1.0) for x in np.arange(0, 10, 0.5)]  # 0 to 10 meters, 0.5m steps

    def simulate_rtk_gps(self, odom_msg):
        """Simulate RTK GPS by adding noise and applying corrections."""
        # Get ground truth position from odometry
        x = odom_msg.pose.pose.position.x
        y = odom_msg.pose.pose.position.y
        
        # Extract orientation (yaw)
        orientation_q = odom_msg.pose.pose.orientation
        (_, _, yaw) = euler_from_quaternion([orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])
        self.current_yaw = yaw
        
        # Simulate standard GPS with noise
        gps_x = x + np.random.normal(0, self.GPS_NOISE)
        gps_y = y + np.random.normal(0, self.GPS_NOISE)
        
        # Simulate RTK correction
        rtk_x = x + np.random.normal(0, self.RTK_PRECISION)
        rtk_y = y + np.random.normal(0, self.RTK_PRECISION)
        
        self.current_position = (rtk_x, rtk_y)
        
        # Publish simulated RTK GPS data
        gps_msg = NavSatFix()
        gps_msg.header.stamp = self.get_clock().now().to_msg()
        gps_msg.header.frame_id = "world"
        gps_msg.latitude = rtk_x  # Simplified: using x, y as lat, lon for simulation
        gps_msg.longitude = rtk_y
        self.gps_pub.publish(gps_msg)

    def control_vehicle(self):
        """Simple PID controller to follow waypoints using RTK GPS position."""
        if not self.current_position or not self.waypoints:
            return
        
        # Find the closest waypoint
        distances = [np.sqrt((self.current_position[0] - wp[0])**2 + (self.current_position[1] - wp[1])**2) 
                     for wp in self.waypoints]
        target_idx = np.argmin(distances)
        target_wp = self.waypoints[target_idx]
        
        # Calculate error
        distance_error = distances[target_idx]
        angle_to_wp = np.arctan2(target_wp[1] - self.current_position[1], 
                                target_wp[0] - self.current_position[0])
        angle_error = angle_to_wp - self.current_yaw
        
        # Normalize angle error to [-pi, pi]
        angle_error = (angle_error + np.pi) % (2 * np.pi) - np.pi
        
        # Simple PID-like control for Ackermann robot
        LINEAR_SPEED = 0.5  # m/s
        Kp_steering = 1.0   # Proportional gain for steering
        
        cmd = Twist()
        if distance_error > 0.1:  # Move if not close to waypoint
            cmd.linear.x = LINEAR_SPEED
            cmd.angular.z = Kp_steering * angle_error
        else:
            # Move to next waypoint or stop
            if target_idx < len(self.waypoints) - 1:
                self.waypoints.pop(0)
            else:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.get_logger().info("Reached final waypoint!")
        
        self.cmd_pub.publish(cmd)

    def odom_callback(self, msg):
        """Callback for odometry data from Gazebo."""
        self.simulate_rtk_gps(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RTKFarmNavigation()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
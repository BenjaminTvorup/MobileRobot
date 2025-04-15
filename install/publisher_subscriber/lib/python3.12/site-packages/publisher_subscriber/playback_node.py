# Import necessary ROS 2 libraries and message types
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped  # Updated to TwistStamped
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import numpy as np
import os

class PlaybackNode(Node):
    def __init__(self):
        super().__init__('playback_node')
        
        # Define the directory where the saved motion data is stored
        self.vector_dir = os.path.expanduser("~/ws_new/vectors")
        
        # Load previously saved motion data (state, velocities, and time)
        try:
            self.state = np.load(os.path.join(self.vector_dir, 'state.npy'))
            self.velocities = np.load(os.path.join(self.vector_dir, 'velocities.npy'))
            self.t = np.load(os.path.join(self.vector_dir, 'time.npy'))
        except FileNotFoundError as e:
            self.get_logger().error(f"Failed to load vectors: {e}")
            raise
        
        self.N = len(self.t)
        self.index = 0
        
        # Create a publisher for TwistStamped messages on the correct topic
        self.vel_pub = self.create_publisher(
            TwistStamped, 
            '/ackermann_steering_controller/reference', 
            10
        )
        
        # Create a broadcaster for TF
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Timer at 10 Hz (0.1 seconds)
        self.timer = self.create_timer(0.1, self.playback_step)
        
        self.get_logger().info(f"Loaded {self.N} data points. Starting playback...")

    def playback_step(self):
        """Replay recorded motion by publishing TwistStamped messages"""
        if self.index < self.N:
            # Get current position and velocity
            x, y, theta = self.state[self.index]
            x_dot, y_dot, theta_dot = self.velocities[self.index]
            
            # Create a TwistStamped message
            vel_msg = TwistStamped()
            vel_msg.header.stamp = self.get_clock().now().to_msg()  # Add timestamp
            vel_msg.header.frame_id = 'base_link'  # Frame ID (adjust if needed)
            vel_msg.twist.linear.x = x_dot
            vel_msg.twist.linear.y = y_dot
            vel_msg.twist.angular.z = theta_dot  # For Ackermann, this is steering rate
            self.vel_pub.publish(vel_msg)
            
            # Publish TF (odom -> base_link)
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'odom'
            t.child_frame_id = 'base_link'
            t.transform.translation.x = x
            t.transform.translation.y = y
            t.transform.translation.z = 0.0
            t.transform.rotation.z = np.sin(theta / 2.0)
            t.transform.rotation.w = np.cos(theta / 2.0)
            self.tf_broadcaster.sendTransform(t)
            
            # Log playback step
            self.get_logger().info(
                f"Step {self.index}/{self.N}: "
                f"x={x:.2f}, y={y:.2f}, theta={theta:.2f}, "
                f"x_dot={x_dot:.2f}, y_dot={y_dot:.2f}, theta_dot={theta_dot:.2f}"
            )
            
            self.index += 1
        else:
            self.get_logger().info("Playback complete")
            self.timer.destroy()

def main(args=None):
    rclpy.init(args=args)
    node = PlaybackNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
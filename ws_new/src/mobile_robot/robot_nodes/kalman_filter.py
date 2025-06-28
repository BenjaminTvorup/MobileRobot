#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
import numpy as np

class KalmanFilterNode(Node):
    def __init__(self):
        super().__init__('kalman_filter_node')
        # State: [x, y, vx, vy]
        self.state = np.zeros((4, 1))  # Initial state
        self.P = np.eye(4) * 1.0  # Initial covariance
        self.F = np.array([[1, 0, 0.1, 0],  # State transition (dt=0.1s)
                           [0, 1, 0, 0.1],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        self.H = np.array([[1, 0, 0, 0],  # Measurement model (position only)
                           [0, 1, 0, 0]])
        self.R = np.eye(2) * 0.1  # Measurement noise covariance
        self.Q = np.eye(4) * 0.01  # Process noise covariance

        # Subscribers and Publishers
        self.sub = self.create_subscription(
            PointStamped, '/sensor/position', self.measurement_callback, 10)
        self.pub = self.create_publisher(PointStamped, '/kf/estimate', 10)
        self.timer = self.create_timer(0.1, self.predict)

        self.get_logger().info('Linear Kalman Filter Node started')

    def predict(self):
        # Predict step
        self.state = self.F @ self.state
        self.P = self.F @ self.P @ self.F.T + self.Q

    def measurement_callback(self, msg):
        # Update step
        z = np.array([[msg.point.x], [msg.point.y]])
        y = z - self.H @ self.state  # Measurement residual
        S = self.H @ self.P @ self.H.T + self.R  # Innovation covariance
        K = self.P @ self.H.T @ np.linalg.inv(S)  # Kalman gain
        self.state = self.state + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P

        # Publish estimated state
        estimate = PointStamped()
        estimate.header = msg.header
        estimate.point.x = float(self.state[0, 0])
        estimate.point.y = float(self.state[1, 0])
        self.pub.publish(estimate)

def main(args=None):
    rclpy.init(args=args)
    node = KalmanFilterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

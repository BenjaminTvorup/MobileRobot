import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose


def calculate_new_position(x, y, distance=0.1):
    new_x = x
    new_y = y + distance
    return new_x, new_y


class GpsSaveXySubscriber(Node):
    def __init__(self):
        super().__init__('gps_save_xy_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            '/odometry/gps',
            self.gps_callback,
            10
        )
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.received = False

    def gps_callback(self, msg):
        if not self.received:
            x = msg.pose.pose.position.x
            y = msg.pose.pose.position.y
            self.get_logger().info(f"Current position: x = {x}, y = {y}")

            x_new, y_new = calculate_new_position(x, y, distance=2.0)
            self.get_logger().info(f"Target position: x = {x_new}, y = {y_new}")

            # Create the goal pose
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = self.get_clock().now().to_msg()
            goal_pose.pose.position.x = x_new
            goal_pose.pose.position.y = y_new
            goal_pose.pose.position.z = 0.0
            goal_pose.pose.orientation.w = 1.0

            # Send the goal
            self.send_goal(goal_pose)
            self.received = True

    def send_goal(self, pose):
        if not self.action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error("NavigateToPose action server not available after 5 seconds")
            return

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose
        self.get_logger().info("Sending goal to NavigateToPose action server")
        send_goal_future = self.action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Goal was rejected by the server")
            return
        self.get_logger().info("Goal accepted, navigating to target position")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"Navigation completed with status: {result}")
        # Optionally shut down after navigation completes
        # rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    gps_subscriber = GpsSaveXySubscriber()
    rclpy.spin(gps_subscriber)
    gps_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
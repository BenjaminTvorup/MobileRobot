import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose

def calculate_new_position(x, y, distance=0.1):
    return x, y + distance

class GpsSaveXySubscriber(Node):
    def __init__(self):
        super().__init__('gps_save_xy_subscriber')
        self.set_parameters([rclpy.Parameter('use_sim_time', rclpy.Parameter.Type.BOOL, True)])
        self.subscription = self.create_subscription(
            Odometry,
            '/odometry/gps',
            self.gps_callback,
            10
        )
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.received = False
        self.goal_pose = None
        self.timer = None

    def gps_callback(self, msg):
        if self.received:
            return

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.get_logger().info(f"Current position: x = {x}, y = {y}")

        x_new, y_new = calculate_new_position(x, y, distance=0.1)
        self.get_logger().info(f"Target position: x = {x_new}, y = {y_new}")

        # Create goal
        self.goal_pose = PoseStamped()
        self.goal_pose.header.frame_id = 'map'  # odom /odometry/gps  / using slam use mapss
        self.goal_pose.header.stamp = self.get_clock().now().to_msg()
        self.goal_pose.pose.position.x = x_new
        self.goal_pose.pose.position.y = y_new
        self.goal_pose.pose.orientation.w = 1.0

        self.received = True
        self.timer = self.create_timer(5.0, self.send_delayed_goal)

    def send_delayed_goal(self):
        self.timer.cancel()
        self.send_goal(self.goal_pose)

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

def main(args=None):
    rclpy.init(args=args)
    node = GpsSaveXySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

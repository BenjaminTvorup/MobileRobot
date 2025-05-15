import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped
from robot_localization.srv import FromLL

class GPSWaypointSender(Node):
    def __init__(self):
        super().__init__('gps_waypoint_sender')
        self.from_ll_client = self.create_client(FromLL, '/fromLL')
        self.action_client = ActionClient(self, FollowWaypoints, 'follow_waypoints')

        # Wait for services and actions to be available
        self.from_ll_client.wait_for_service()
        self.action_client.wait_for_server()

    def send_gps_waypoints(self, gps_waypoints):
        # Convert each GPS waypoint to a PoseStamped message in the map frame
        poses = []
        for lat, lon in gps_waypoints:
            # Call the fromLL service to convert GPS to map coordinates
            req = FromLL.Request()
            req.ll_point.latitude = lat
            req.ll_point.longitude = lon
            req.ll_point.altitude = 0.0  # Assuming ground level
            future = self.from_ll_client.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            map_point = future.result().map_point

            # Create a PoseStamped message
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.pose.position.x = map_point.x
            pose.pose.position.y = map_point.y
            pose.pose.position.z = 0.0
            pose.pose.orientation.w = 1.0  # Default orientation (no rotation)
            poses.append(pose)

        # Send the waypoints to the waypoint follower
        goal_msg = FollowWaypoints.Goal()
        goal_msg.poses = poses
        self.action_client.send_goal_async(goal_msg)
        self.get_logger().info('Sent waypoints to the robot!')

def main():
    rclpy.init()
    node = GPSWaypointSender()
    
    # Example GPS waypoints (replace with your coordinates)
    gps_waypoints = [
        (40.7128, -74.0060),  # Example: New York City
        (34.0522, -118.2437)  # Example: Los Angeles
    ]
    
    node.send_gps_waypoints(gps_waypoints)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
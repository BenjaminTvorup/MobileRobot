import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class GpsSubscriber(Node):
    def __init__(self):
        # Initialize the node with a name
        super().__init__('gps_subscriber')
        
        # Create a subscription to the /odometry/gps topic
        self.subscription = self.create_subscription(
            Odometry,              # Message type
            '/odometry/gps',       # Topic name
            self.gps_callback,     # Callback function
            10                     # Queue size
        )
        self.subscription  # Prevent unused variable warning

    def gps_callback(self, msg):
        # Print the entire message, similar to ros2 topic echo
        print(msg)

def main(args=None):
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)
    
    # Create the node
    gps_subscriber = GpsSubscriber()
    
    # Keep the node running to process messages
    rclpy.spin(gps_subscriber)
    
    # Clean up when the node is shut down (e.g., with Ctrl+C)
    gps_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
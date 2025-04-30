import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry




def calculate_new_position(x, y, distance=2.0):
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
        self.received = False

    def gps_callback(self, msg):
        if not self.received:
            x = msg.pose.pose.position.x
            y = msg.pose.pose.position.y
            print(f"x = {x}, y = {y}")

            x_new,y_new = calculate_new_position(x, y, distance=2.0)
            print(f"x = {x_new}, y = {y_new}")

            rclpy.shutdown()




def main(args=None):
    rclpy.init(args=args)
    gps_subscriber = GpsSaveXySubscriber()
    rclpy.spin(gps_subscriber)
    gps_subscriber.destroy_node()

if __name__ == '__main__':
    main()
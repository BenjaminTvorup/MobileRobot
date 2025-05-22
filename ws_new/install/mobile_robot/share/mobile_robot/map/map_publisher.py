import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
import yaml
from PIL import Image
import numpy as np

class MapPublisher(Node):
    def __init__(self, map_yaml_path):
        super().__init__('map_publisher')
        self.map_yaml_path = map_yaml_path
        self.map_pub = self.create_publisher(OccupancyGrid, '/map', 10)
        self.timer = self.create_timer(1.0, self.load_and_publish_map)
        self.get_logger().info('Map publisher node started')

    def load_and_publish_map(self):
        # Load map metadata from YAML file
        with open(self.map_yaml_path, 'r') as f:
            map_meta = yaml.safe_load(f)

        # Load the map image (e.g., .pgm)
        map_img = Image.open(map_meta['image']).convert('L')  # Convert to grayscale
        map_data = np.array(map_img)

        # Remap grayscale values (0-255) to occupancy grid values (-1, 0, 100)
        map_data = np.where(map_data == 255, 0, 100)  # Free space (0) and occupied space (100)
        map_data = map_data.flatten().astype(np.int8).tolist()  # Flatten and convert to signed 8-bit integers

        # Create and populate OccupancyGrid message
        grid = OccupancyGrid()
        grid.header.frame_id = 'map'
        grid.header.stamp = self.get_clock().now().to_msg()
        grid.info.resolution = map_meta['resolution']
        grid.info.width = map_img.width
        grid.info.height = map_img.height
        grid.info.origin.position.x = map_meta['origin'][0]
        grid.info.origin.position.y = map_meta['origin'][1]
        grid.info.origin.position.z = 0.0
        grid.data = map_data  # Flattened map data

        # Publish the map
        self.map_pub.publish(grid)
        self.get_logger().info('Map published to /map')

def main(args=None):
    rclpy.init(args=args)
    map_yaml_path = 'src/mobile_robot/map/empty_map.yaml'  # Replace with your map file path

    # Instantiate the MapPublisher node
    map_publisher = MapPublisher(map_yaml_path)

    try:
        rclpy.spin(map_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        map_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav2_controller.controller_server import ControllerServer

class ControllerServerNode(Node):
    def __init__(self):
        super().__init__('controller_server')

        # Declare all parameters from Controller Server documentation
        self.declare_parameter('controller_frequency', 20.0)
        self.declare_parameter('costmap_update_timeout', 0.3)
        self.declare_parameter('use_realtime_priority', False)
        self.declare_parameter('publish_zero_velocity', True)
        self.declare_parameter('action_server_result_timeout', 10.0)
        self.declare_parameter('controller_plugins', ['FollowPath'])
        self.declare_parameter('FollowPath.plugin', 'nav2_regulated_pure_pursuit_controller/RegulatedPurePursuitController')
        self.declare_parameter('progress_checker_plugins', ['progress_checker'])
        self.declare_parameter('progress_checker.plugin', 'nav2_controller::SimpleProgressChecker')
        self.declare_parameter('goal_checker_plugins', ['goal_checker'])
        self.declare_parameter('goal_checker.plugin', 'nav2_controller::SimpleGoalChecker')
        self.declare_parameter('min_x_velocity_threshold', 0.0001)
        self.declare_parameter('min_y_velocity_threshold', 0.0001)
        self.declare_parameter('min_theta_velocity_threshold', 0.0001)
        self.declare_parameter('failure_tolerance', 0.0)
        self.declare_parameter('speed_limit_topic', 'speed_limit')
        self.declare_parameter('odom_topic', 'odom')
        self.declare_parameter('enable_stamped_cmd_vel', False)  # False for Jazzy compatibility
        self.declare_parameter('bond_heartbeat_period', 0.1)

        # Additional parameters for RegulatedPurePursuitController
        self.declare_parameter('FollowPath.desired_linear_vel', 0.5)
        self.declare_parameter('FollowPath.max_linear_vel', 0.7)
        self.declare_parameter('FollowPath.min_linear_vel', 0.1)
        self.declare_parameter('FollowPath.max_angular_vel', 1.0)
        self.declare_parameter('FollowPath.max_linear_accel', 2.5)
        self.declare_parameter('FollowPath.max_linear_decel', 2.5)
        self.declare_parameter('FollowPath.max_angular_accel', 3.2)
        self.declare_parameter('FollowPath.lookahead_dist', 0.6)
        self.declare_parameter('FollowPath.min_lookahead_dist', 0.3)
        self.declare_parameter('FollowPath.max_lookahead_dist', 1.0)
        self.declare_parameter('FollowPath.lookahead_time', 1.5)
        self.declare_parameter('FollowPath.transform_tolerance', 0.2)
        self.declare_parameter('FollowPath.use_velocity_scaled_lookahead_dist', True)
        self.declare_parameter('FollowPath.min_approach_linear_velocity', 0.05)
        self.declare_parameter('FollowPath.use_collision_detection', True)
        self.declare_parameter('FollowPath.use_regulated_linear_velocity_scaling', True)
        self.declare_parameter('FollowPath.use_cost_regulated_linear_velocity_scaling', True)
        self.declare_parameter('FollowPath.regulated_linear_scaling_min_radius', 0.5)
        self.declare_parameter('FollowPath.regulated_linear_scaling_min_speed', 0.1)
        self.declare_parameter('FollowPath.use_rotate_to_heading', True)
        self.declare_parameter('FollowPath.max_rotational_vel', 0.5)
        self.declare_parameter('FollowPath.min_rotational_vel', 0.05)
        self.declare_parameter('FollowPath.rotate_to_heading_angular_vel', 0.5)
        self.declare_parameter('use_sim_time', True)

        # Initialize the ControllerServer
        self.controller_server = ControllerServer(self)

    def destroy_node(self):
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ControllerServerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
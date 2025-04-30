#include <rclcpp/rclcpp.hpp>                  // Core ROS2 library (system header)
#include "sensor_msgs/msg/joint_state.hpp"    // JointState message header
#include "nav_msgs/msg/odometry.hpp"          // Odometry message header
#include <tf2_ros/transform_broadcaster.h>     // TF2 ROS broadcaster header
#include <tf2/LinearMath/Quaternion.h>         // TF2 Quaternion header
#include <geometry_msgs/msg/transform_stamped.hpp> // TransformStamped message header
#include <cmath>                              // Math functions

class KinematicsNode : public rclcpp::Node {
public:
    KinematicsNode() : Node("kinematics_node"), x_(0.0), y_(0.0), theta_(0.0), last_time_(0, 0, get_clock()->get_clock_type()) {
        sub_ = create_subscription<sensor_msgs::msg::JointState>(
            "/joint_states", 10, std::bind(&KinematicsNode::callback, this, std::placeholders::_1));
        pub_ = create_publisher<nav_msgs::msg::Odometry>("/odom_my", 10);
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
    }
private:
    void callback(const sensor_msgs::msg::JointState::SharedPtr msg) {
        // Check if the incoming message has a valid timestamp.
        // If not valid, you might want to fallback to the current time.
        rclcpp::Time current_time = msg->header.stamp;
        if (current_time.nanoseconds() == 0) {
            current_time = this->get_clock()->now();
        }

        // If it's the first message, store the time and return without computation.
        if (last_time_.nanoseconds() == 0) {
            last_time_ = current_time;
            return;
        }

        // Calculate time difference between the current and last message.
        double dt = (current_time - last_time_).seconds();
        last_time_ = current_time;

        // Retrieve joint values:
        // Assumes that joint_states has the steering angles at indexes 2 and 4
        // and the rear wheel velocities at indexes 0 and 1.
        double delta = (msg->position[2] + msg->position[4]) / 2.0; // Average steering angle
        double w_left = msg->velocity[0];  // Rear left wheel (bl_wheel_joint)
        double w_right = msg->velocity[1]; // Rear right wheel (br_wheel_joint)
        double r = 0.235; // Rear wheel radius (meters)
        double L = 1.364; // Wheelbase (meters)
        double v = (w_left + w_right) / 2.0 * r; // Linear velocity (meters per second)
        double omega = (v / L) * std::tan(delta);   // Angular velocity (radians per second)

        // Update the robot's pose using simple kinematics:
        theta_ += omega * dt;
        x_ -= v * std::cos(theta_) * dt;
        y_ -= v * std::sin(theta_) * dt;

        // Publish odometry message:
        nav_msgs::msg::Odometry odom;
        odom.header.stamp = current_time;  // Use the current time stamp for odometry message
        odom.header.frame_id = "odom";
        odom.child_frame_id = "base_link";
        odom.pose.pose.position.x = x_;
        odom.pose.pose.position.y = y_;
        odom.pose.pose.position.z = 0.0;

        tf2::Quaternion q;
        q.setRPY(0, 0, theta_);
        odom.pose.pose.orientation.x = q.x();
        odom.pose.pose.orientation.y = q.y();
        odom.pose.pose.orientation.z = q.z();
        odom.pose.pose.orientation.w = q.w();

        odom.twist.twist.linear.x = v;
        odom.twist.twist.angular.z = omega;

        // Set covariance values
        for (int i = 0; i < 36; ++i) {
            if (i == 0) {
                if (std::abs(v) <= 0.05) {
                    odom.twist.covariance[i] = 0.000001;
                } else {
                    odom.twist.covariance[i] = 0.0001;
                }
            } else if (i == 7) {
                if (std::abs(v) <= 0.05) {
                    odom.twist.covariance[i] = 0.0001;
                } else {
                    odom.twist.covariance[i] = 0.001;
                }
            } else if (i == 35) {
                if (std::abs(omega) <= 0.05) {
                    odom.twist.covariance[i] = 0.00001;
                } else {
                    odom.twist.covariance[i] = 0.05;
                }
            } else if (i == 14 || i == 21 || i == 28) {
                odom.twist.covariance[i] = 99999.0;
            } else {
                odom.twist.covariance[i] = 0.0;
            }
        }

        pub_->publish(odom);

        // Publish TF transform:
        geometry_msgs::msg::TransformStamped tf;
        tf.header.stamp = current_time;
        tf.header.frame_id = "odom";
        tf.child_frame_id = "base_link";
        tf.transform.translation.x = x_;
        tf.transform.translation.y = y_;
        tf.transform.translation.z = 0.0;
        tf.transform.rotation = odom.pose.pose.orientation;
        tf_broadcaster_->sendTransform(tf);
    }
    
    rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr sub_;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr pub_;
    std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
    double x_, y_, theta_;
    rclcpp::Time last_time_;  // Store previous timestamp for dt computation
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<KinematicsNode>());
    rclcpp::shutdown();
    return 0;
}

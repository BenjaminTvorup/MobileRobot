import numpy as np

class NoisyOdometry:
    def __init__(self, wheelbase=0.3, dt=0.1, noise_scale=0.02):
        """
        Initialize noisy odometry model for differential drive robot.
        wheelbase: Distance between wheels (m)
        dt: Time step (s)
        noise_scale: Noise standard deviation as fraction of wheel velocity
        """
        self.L = wheelbase
        self.dt = dt
        self.noise_scale = noise_scale
        self.state = np.array([0.0, 0.0, 0.0])  # [x, y, theta]

    def add_noise(self, v_l, v_r):
        """Add Gaussian noise to wheel velocities."""
        sigma_l = self.noise_scale * abs(v_l)
        sigma_r = self.noise_scale * abs(v_r)
        noise_l = np.random.normal(0, sigma_l)
        noise_r = np.random.normal(0, sigma_r)
        return v_l + noise_l, v_r + noise_r

    def update(self, v_l_nominal, v_r_nominal):
        """Update robot pose with noisy odometry."""
        # Add noise to wheel velocities
        v_l, v_r = self.add_noise(v_l_nominal, v_r_nominal)

        # Compute noisy linear and angular velocities
        v = (v_r + v_l) / 2.0
        omega = (v_r - v_l) / self.L

        # Update pose
        x, y, theta = self.state
        x += v * self.dt * np.cos(theta)
        y += v * self.dt * np.sin(theta)
        theta += omega * self.dt

        # Normalize theta to [-pi, pi]
        theta = np.arctan2(np.sin(theta), np.cos(theta))
        self.state = np.array([x, y, theta])

        return self.state

    def get_pose(self):
        """Return current pose [x, y, theta]."""
        return self.state

# Example usage
if __name__ == "__main__":
    odom = NoisyOdometry(wheelbase=0.3, dt=0.1, noise_scale=0.02)
    trajectory = []

    # Simulate 100 steps with constant wheel velocities
    for _ in range(100):
        v_l, v_r = 0.5, 0.5  # Move straight at 0.5 m/s
        pose = odom.update(v_l, v_r)
        trajectory.append(pose.copy())

    # Print final pose
    print(f"Final pose: x={pose[0]:.2f}, y={pose[1]:.2f}, theta={pose[2]:.2f}")

    # Optional: Plot trajectory (requires matplotlib)
    import matplotlib.pyplot as plt
    trajectory = np.array(trajectory)
    plt.plot(trajectory[:, 0], trajectory[:, 1], label="Noisy Odometry")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("noisy_odometry_trajectory.png")

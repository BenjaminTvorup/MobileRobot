import numpy as np
import matplotlib.pyplot as plt

# Load the saved data
state = np.load('state.npy')  # [x, y, theta]
t = np.load('time.npy')       # time vector

# Extract x and y positions
x = state[:, 0]
y = state[:, 1]

# Create a single plot
plt.figure(figsize=(10, 6))
plt.plot(t, x, 'b-', label='X Position')
plt.plot(t, y, 'r-', label='Y Position')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('X and Y Position vs Time')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
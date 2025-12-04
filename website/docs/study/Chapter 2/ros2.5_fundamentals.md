# 2.5 Practical ROS 2 Setup for Humanoid Development
## Recommended Development Environment

```bash
---

# 1. Install ROS 2 Humble (Ubuntu 22.04)
sudo apt install ros-humble-desktop

# 2. Create humanoid-specific workspace
mkdir -p ~/humanoid_ws/src
cd ~/humanoid_ws
colcon build

# 3. Essential packages for humanoids
# Control
sudo apt install ros-humble-control-toolbox
sudo apt install ros-humble-ros2-control
# Perception
sudo apt install ros-humble-vision-opencv
sudo apt install ros-humble-perception-pcl
# Simulation
sudo apt install ros-humble-gazebo-ros-pkgs
```
---

```text 
humanoid_robot/
├── config/
│   ├── controllers.yaml      # PID gains, control parameters
│   ├── urdf/                 # Robot description files
│   └── rviz/                 # Visualization configs
├── launch/
│   ├── simulation.launch.py  # Gazebo + RViz
│   ├── hardware.launch.py    # Real robot interface
│   └── perception.launch.py  # Camera + AI nodes
├── scripts/
│   ├── calibration.py        # Sensor calibration
│   ├── walk_test.py          # Gait testing
│   └── ai_agent.py          # ML model integration
└── src/
    ├── control/              # Balance, walking controllers
    ├── perception/           # Vision, object detection
    ├── planning/             # Motion planning
    └── utils/               # Common utilities
---

## 2.6 Case Study: ROS 2 in Commercial Humanoids

### Tesla Optimus ROS Architecture
While Tesla uses proprietary software, analysis suggests a ROS 2-like architecture:

**Multi-rate Control Loops**
- **High-frequency (1kHz):** Joint-level control
- **Medium-frequency (100Hz):** Balance and locomotion
- **Low-frequency (10Hz):** Task planning

**Distributed Processing**
- Onboard computers for real-time control
- Offboard computation for AI/ML
- Cloud integration for fleet learning

### Unitree H1 Open-Source Example
Unitree provides ROS 2 interfaces for their humanoid, demonstrating:

```yaml
# Example: Unitree H1 ROS 2 Control Interface
control_modes:
  position:    # For precise manipulation
    frequency: 500Hz
    joints: arm, hand
  torque:      # For locomotion
    frequency: 1000Hz
    joints: leg
  impedance:   # For interaction
    frequency: 500Hz
    joints: all
```

---

## 2.7 Hands-On Exercise: Building a Simple Humanoid ROS 2 System

### **Exercise 1: Create a Minimal Humanoid URDF**
**Objective:** Create a 12-DOF humanoid (6 per leg) URDF model

```xml
<!-- Step-by-step URDF development -->
1. Create base link (pelvis)
2. Add left leg chain: hip_yaw → hip_roll → hip_pitch → knee → ankle_pitch → ankle_roll
3. Mirror for right leg
4. Add simple visual and collision geometry
5. Define joint limits based on human biomechanics
```

### **Exercise 2: ROS 2 Node for Joint State Visualization**

```python
# Complete this node to visualize joint states
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import matplotlib.pyplot as plt

class JointStateVisualizer(Node):
    def __init__(self):
        super().__init__('joint_state_viz')
        # TODO: Create subscription to /joint_states
        # TODO: Store last 100 samples of each joint
        # TODO: Create real-time plot updating at 10Hz
        
    def joint_state_callback(self, msg):
        # TODO: Extract joint positions
        # TODO: Update plot data
        pass
```

### **Exercise 3: Bridge OpenAI Gym to ROS 2**

```python
# Framework for RL training in simulation
class HumanoidGymEnv:
    def __init__(self, ros_node):
        self.node = ros_node
        self.setup_action_space()
        self.setup_observation_space()
    
    def step(self, action):
        # 1. Convert action to ROS joint commands
        # 2. Publish commands
        # 3. Wait for next observation
        # 4. Calculate reward
        # 5. Return (obs, reward, done, info)
        pass
```

---

## 2.8 Common Pitfalls and Best Practices

### **Performance Optimization**

#### Avoid Blocking Calls in Callbacks

```python
# BAD: Blocking network call in callback
def camera_callback(self, msg):
    result = slow_ai_inference(msg.data)  # Blocks!
    
# GOOD: Use async or worker threads
def camera_callback(self, msg):
    self.executor.create_task(self.async_inference, msg)
```

### **QoS Settings for Critical Data**

```python
# IMU data needs reliability
qos_profile = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    depth=10
)
self.imu_sub = self.create_subscription(
    Imu, '/imu', callback, qos_profile)
```

### **Debugging Tools**

```bash
# Essential ROS 2 debugging commands
ros2 topic list -t           # List all topics with types
ros2 topic echo /joint_states  # View topic data
ros2 node info /walking_controller  # Node connections
ros2 bag record -a           # Record all topics
ros2 run rqt_graph rqt_graph # Visualize node graph
```

---

## 2.9 Learning Objectives Recap
By completing this chapter, you should be able to:

- Explain the role of ROS 2 in humanoid robot software architecture
- Design a URDF model for a basic humanoid robot
- Implement ROS 2 nodes that bridge AI models with physical control
- Configure appropriate QoS settings for different data types in humanoids
- Debug ROS 2 systems using standard command-line tools
- Structure a humanoid robot project with proper ROS 2 conventions

---

## 2.10 Additional Resources

### **Official Documentation**
- ROS 2 Documentation https://docs.ros.org/
- URDF Tutorials  http://wiki.ros.org/urdf/Tutorials
- ROS 2 Control https://control.ros.org/

### **Community Resources**
- ROS Discourse https://discourse.ros.org/
- ROS Answers https://answers.ros.org/
- Humanoid Robotics ROS Packages https://github.com/ros-humanoid

### **Recommended Books**
- Koubaa, A. (2022). *Robot Operating System (ROS) 2: The Complete Reference*. Springer.
- Joseph, L. (2022). *ROS 2 Robotics Projects (2nd ed.)*. Packt Publishing.

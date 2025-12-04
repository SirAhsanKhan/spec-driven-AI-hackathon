# Chapter 3: The Digital Twin — Simulation with Gazebo & Unity (Part 1)

## 3.1 Introduction to Robotic Simulation
### Why Simulation is Critical for Humanoid Development
Simulation is essential for humanoid robotics because it enables:
- **Safety**: Prevents dangerous or damaging tests on real hardware.
- **Cost Efficiency**: Avoids costly repairs ($10K–$50K per major failure).
- **Scalability**: Allows thousands of tests to run in parallel.

> "Simulation isn't just a convenience—it's a necessity for developing complex systems like humanoids. The cost and risk of physical testing alone would make progress impossible." — DARPA Robotics Challenge Report, 2015

### The Reality Gap Revisited
Despite its strengths, simulation introduces discrepancies between simulated and real conditions:
- **Contact Dynamics**: Foot-ground interactions are difficult to simulate
- **Actuator Dynamics**: Real actuators have friction, saturation, non-linearities
- **Sensor Noise**: Real sensors exhibit drift, noise, and imperfect data
- **Timing Differences**: Real time vs. simulation step-timing differences

---

## 3.2 Gazebo: Physics-Based Simulation
### Setting Up Gazebo for Humanoid Simulation

#### Installation and Configuration
```bash
sudo apt install ros-humble-gazebo-ros-pkgs\sudo apt install gazebo11
sudo apt install gazebo11-plugin-bullet\sudo apt install gazebo11-plugin-dartsim

gazebo --version
```

#### Recommended Configuration for Humanoids
```bash
export GAZEBO_MODEL_PATH=$HOME/humanoid_ws/src/models:$GAZEBO_MODEL_PATH
export GAZEBO_RESOURCE_PATH=$HOME/humanoid_ws/src/worlds:$GAZEBO_RESOURCE_PATH
export GAZEBO_PLUGIN_PATH=$HOME/humanoid_ws/build:$GAZEBO_PLUGIN_PATH

export GAZEBO_PHYSICS_ENGINE=ode
export GAZEBO_MAX_STEP_SIZE=0.001
export GAZEBO_REALTIME_FACTOR=1.0
```

### Physics Engine Comparison
| Physics Engine | Strengths | Weaknesses | Best For |
|----------------|-----------|------------|-----------|
| **ODE** | Stable, mature | Conservative contact | Walking |
| **Bullet** | Great contact accuracy | Weaker joint accuracy | Manipulation |
| **DART** | Biomechanically accurate | Expensive | Dynamic motion |
| **MuJoCo** | Very high fidelity | Commercial | Research |

---

### Creating Realistic Humanoid Environments
#### Example: Stair Climbing World
```xml
<sdf version="1.6">
  <world name="stair_climbing">
    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>

    <!-- Stairs and obstacles here -->

    <physics name="humanoid_physics" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <ode>
        <solver>
          <type>quick</type>
          <iters>50</iters>
        </solver>
      </ode>
    </physics>
  </world>
</sdf>
```

---

## 3.3 Sensor Simulation in Gazebo
### IMU Simulation
```xml
<sensor name="imu_sensor" type="imu">
  <update_rate>1000</update_rate>
  <plugin filename="libgazebo_ros_imu_sensor.so" name="imu_plugin">
    <gaussianNoise>0.0004</gaussianNoise>
  </plugin>
</sensor>
```

### Camera Simulation
```xml
<sensor name="depth_camera" type="depth">
  <camera>
    <image><width>640</width><height>480</height></image>
    <noise><stddev>0.007</stddev></noise>
  </camera>
</sensor>
```

### Force-Torque Sensor Simulation
```xml
<plugin name="ft_sensor_plugin" filename="libgazebo_ros_ft_sensor.so">
  <noise><force><stddev>5</stddev></force></noise>
</plugin>
```

---

## 3.4 Unity for High-Fidelity Simulation
### Unity vs. Gazebo
| Aspect | Gazebo | Unity |
|--------|--------|--------|
| Physics | High accuracy | Moderate |
| Visuals | Basic | Photo-realistic |
| Best For | Control | Perception, HRI |

### Setting Up Unity
```bash
git clone https://github.com/Unity-Technologies/ROS-TCP-Connector.git
git clone https://github.com/Unity-Technologies/Unity-Robotics-Hub.git
```

### Humanoid Articulation Body Setup
```csharp
ArticulationDrive drive = joint.xDrive;
drive.stiffness = 1000f;
drive.damping = 100f;
joint.xDrive = drive;
```

---

## 3.5 Domain Randomization for Sim-to-Real
### Why It's Essential
Randomization helps policies generalize by varying:
- **Physics**: gravity, friction, damping
- **Visuals**: lighting, textures, noise
- **Environment**: slope, obstacles, compliance
- **Robot Parameters**: mass, torque, joint friction

### Gazebo Domain Randomization Example
```python
req.gravity.z = np.random.uniform(4.9, 14.7)
ode_config.cfm = np.random.uniform(0.000001, 0.001)
```


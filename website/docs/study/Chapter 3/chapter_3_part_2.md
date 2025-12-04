# Chapter 3: The Digital Twin — Simulation with Gazebo & Unity (Part 2)

## 3.6 Simulation Benchmarks and Performance Metrics

### Standardized Testing Environments

#### 1. Locomotion Benchmark Suite
```yaml
tests:
  - name: flat_ground_walking
    duration: 60
    success_criteria:
      max_fall_count: 0
      avg_speed: >0.5
      energy_efficiency: <150

  - name: stair_climbing
    stairs:
      count: 5
      height: 0.15
    success_criteria:
      completion_time: <30

  - name: slope_walking
    slopes: [5, 10, 15]
    success_criteria:
      stability_margin: >0.02
```

#### 2. Manipulation Benchmark Suite
```python
class ManipulationBenchmark:
    def test_door_opening(self):
        metrics = {"success_rate": 0.0}

    def test_object_pickup(self):
        objects = [
            {"name": "small_cube", "size": 0.05},
            {"name": "medium_cylinder", "size": 0.1}
        ]
```

### Performance Metrics
```python
class HumanoidPerformanceMetrics:
    def calculate_zmp_trajectory(...): pass
    def calculate_capture_point(...): pass
    def energy_efficiency(...): pass
```

---

## 3.7 Hands-On Exercises

### Exercise 1: Balancing Controller
```python
class BalanceController:
    def imu_callback(self, msg):
        pass
```

### Exercise 2: Domain Randomization Experiment
```python
results_no_dr = train_with_randomization(False)
results_with_dr = train_with_randomization(True)
```

### Exercise 3: Reality Gap Analysis
```python
gap_percentage = abs(sim - real) / real * 100
```

---

## 3.8 Best Practices for Simulation Development

### 1. Version Control Structure
```
simulation_assets/
├── models/
├── worlds/
├── plugins/
└── scripts/
```

### 2. Simulation Automation
```yaml
name: Simulation Tests
jobs:
  gazebo-tests:
    steps:
      - name: Run tests
        run: pytest
```

### 3. Performance Optimization Tips
```
1. Use simplified collision meshes
2. Reduce physics update rate
3. Disable visualization during training
4. Parallelize simulations
```

---

## 3.9 Learning Objectives Recap
By the end of this chapter, you can:
- Configure Gazebo for humanoids
- Simulate sensors with realistic noise
- Use Unity for high-fidelity rendering
- Apply domain randomization
- Benchmark humanoid locomotion and manipulation
- Measure the reality gap
- Automate simulation workflows

---

## 3.10 Additional Resources
### Official Documentation
- Gazebo Docs http://gazebosim.org/docs
- Unity Robotics Hub https://github.com/Unity-Technologies/Unity-Robotics-Hub
- ROS2 Gazebo Integration https://github.com/ros-simulation/gazebo_ros_pkgs

### Research Papers
- Todorov et al., *MuJoCo*
- Peng et al., *Dynamics Randomization*
- Chebotar et al., *Closing the Sim-to-Real Loop*

### Benchmarks & Datasets
- ROBEL
- Meta-World
- Gibson Environment


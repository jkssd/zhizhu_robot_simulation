# zhizhu_robot_simulation

蜘蛛（zhizhu）机器人的 ROS 2 仿真包：把单个二进制 STL 网格转换为 URDF/SDF，在 RViz 和 Gazebo 中静态显示。

## 环境

- ROS 2 Humble
- Gazebo Classic 11.10.2
- Ubuntu 22.04

## 目录结构

```
.
├── assets/
│   └── assembly.stl                 # 原始 STL（CAD 导出，单位 mm）
└── src/
    └── zhizhu_description/          # ROS 2 包
        ├── package.xml
        ├── CMakeLists.txt
        ├── meshes/zhizhu.stl        # 网格（ASCII 安全名，与 assets/assembly.stl 相同）
        ├── urdf/zhizhu.urdf         # URDF（供 RViz）
        ├── launch/
        │   ├── display.launch.py    # RViz 查看
        │   └── gazebo.launch.py     # Gazebo 加载
        ├── rviz/zhizhu.rviz
        └── worlds/zhizhu.world      # 世界文件（含地面 + 光照 + 模型 SDF）
```

## 构建与运行

```bash
cd zhizhu_robot_simulation
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash

# RViz 查看
ros2 launch zhizhu_description display.launch.py

# Gazebo 显示（模型内嵌在 world 文件里）
ros2 launch zhizhu_description gazebo.launch.py
```

## 模型说明

- 原始网格：单个二进制 STL，35676 三角形，CAD 单位 mm，包围盒约 `3.68 × 1.78 × 0.89 m`。
- URDF / SDF 中的 `scale="0.001 ..."` 把 mm 换算成 m。
- `rpy="3.14159 0 0"`（绕 X 轴滚转 180°）：CAD 导出时模型上下颠倒，翻转后吸盘侧朝上。若需绕另一水平轴翻转，改 URDF 和 world 里的对应 pose。

## 已知问题

- **Gazebo Classic 11.10.2 运行时插入的模型不渲染**：在本环境下，通过 `spawn_entity` / `gz model -f` 动态插入的模型（无论 URDF 还是 SDF、无论 box 还是 mesh）其 visual 都不会显示，而启动时写进 world 文件的模型渲染正常。因此当前 `gazebo.launch.py` 把模型直接内嵌在 `worlds/zhizhu.world` 中，绕开动态 spawn。
- 若后续需要机器人运动（动态 spawn），需先解决上述 Gazebo 运行时插入渲染问题（升级/重装 Gazebo、检查 GPU/OGRE 环境等）。

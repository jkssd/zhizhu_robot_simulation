"""View the zhizhu model in RViz (visual check before Gazebo)."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg = "zhizhu_description"
    urdf_path = os.path.join(get_package_share_directory(pkg), "urdf", "zhizhu.urdf")

    with open(urdf_path, "r") as f:
        robot_description = f.read()

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            os.path.join(get_package_share_directory(pkg), "rviz", "zhizhu.rviz"),
        ],
    )

    return LaunchDescription([robot_state_publisher, rviz])
#ros2 launch zhizhu_description gazebo.launch.py
"""Tripod gait: animate the robot walking (RViz + optional Gazebo)."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
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

    gait = Node(
        package="zhizhu_description",
        executable="gait_node.py",
        name="gait_node",
        parameters=[
            {"stride": 0.04, "lift": 0.03, "speed": 0.6, "rate": 40.0}
        ],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(get_package_share_directory(pkg), "rviz", "zhizhu.rviz")],
    )

    return LaunchDescription([robot_state_publisher, gait, rviz])

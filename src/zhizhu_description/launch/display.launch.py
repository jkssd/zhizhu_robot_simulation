"""View the zhizhu model in RViz."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg = "zhizhu_description"
    xacro_path = os.path.join(get_package_share_directory(pkg), "urdf", "zhizhu.xacro")

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": Command(["xacro", xacro_path])}],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(get_package_share_directory(pkg), "rviz", "zhizhu.rviz")],
    )

    return LaunchDescription([robot_state_publisher, rviz])

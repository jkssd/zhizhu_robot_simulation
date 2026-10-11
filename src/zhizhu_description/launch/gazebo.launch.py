"""Start Gazebo Classic with the zhizhu world + publish TF."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg = "zhizhu_description"
    xacro_path = os.path.join(get_package_share_directory(pkg), "urdf", "zhizhu.xacro")
    world_path = os.path.join(get_package_share_directory(pkg), "worlds", "zhizhu.world")

    joint_state_publisher = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": Command(["xacro", xacro_path])}],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py")
        ),
        launch_arguments={"world": world_path}.items(),
    )

    return LaunchDescription([joint_state_publisher, robot_state_publisher, gazebo])

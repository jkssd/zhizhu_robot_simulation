"""Spawn zhizhu via spawn_entity (for future motion/physics).

NOTE: in headless testing, gazebo_ros 3.9.0 + Gazebo Classic 11.10.2 does not
render visuals of models inserted through /spawn_entity (world-file models do
render). Try this in the GUI — if the model is invisible here too, use
gazebo.launch.py (world-file) instead and see README for the known issue.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg = "zhizhu_description"
    urdf_path = os.path.join(get_package_share_directory(pkg), "urdf", "zhizhu.urdf")
    world_path = os.path.join(get_package_share_directory(pkg), "worlds", "spawn.world")

    with open(urdf_path, "r") as f:
        robot_description = f.read()

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py"
            )
        ),
        launch_arguments={"world": world_path}.items(),
    )

    spawn = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "zhizhu"],
        output="screen",
    )

    return LaunchDescription([robot_state_publisher, gazebo, spawn])

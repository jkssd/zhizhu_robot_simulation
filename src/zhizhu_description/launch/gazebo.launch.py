"""Start Gazebo Classic with the zhizhu world (model embedded directly in it).

The model is embedded in worlds/zhizhu.world as SDF because spawn_entity does
not render visuals in this gazebo_ros 3.9.0 / Gazebo Classic 11 combination.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg = "zhizhu_description"
    world_path = os.path.join(get_package_share_directory(pkg), "worlds", "zhizhu.world")

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py"
            )
        ),
        launch_arguments={"world": world_path}.items(),
    )

    return LaunchDescription([gazebo])

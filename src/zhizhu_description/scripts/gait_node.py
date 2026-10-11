#!/usr/bin/env python3
"""Tripod gait node for the zhizhu hexapod.

Publishes /joint_states from a tripod gait so the robot walks in RViz/Gazebo.
Leg model: hip = yaw (Z), knee = pitch (horizontal, bends the leg),
ankle = roll (wheel axle, kept at 0 for the walking gait).

Tripod groups: A = lf, rm, lr ; B = rf, lm, rr (alternating).
"""
import json
import math
import os

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from ament_index_python.packages import get_package_share_directory


class GaitNode(Node):
    def __init__(self):
        super().__init__("gait_node")

        pkg = "zhizhu_description"
        params_path = os.path.join(
            get_package_share_directory(pkg), "config", "leg_params.json"
        )
        with open(params_path) as f:
            self.legs = json.load(f)

        self.leg_names = ["lf", "lm", "lr", "rf", "rm", "rr"]
        self.joint_names = []
        for nm in self.leg_names:
            self.joint_names += [f"hip_{nm}", f"knee_{nm}", f"ankle_{nm}"]

        self.declare_parameter("stride", 0.04)
        self.declare_parameter("lift", 0.03)
        self.declare_parameter("rate", 40.0)
        self.declare_parameter("speed", 0.6)

        self.stride = self.get_parameter("stride").value
        self.lift = self.get_parameter("lift").value
        self.speed = self.get_parameter("speed").value

        self.group_A = ["lf", "rm", "lr"]
        self.group_B = ["rf", "lm", "rr"]
        self.phase = {}
        for nm in self.leg_names:
            self.phase[nm] = 0.0 if nm in self.group_A else math.pi

        self.pub = self.create_publisher(JointState, "/joint_states", 10)
        rate = self.get_parameter("rate").value
        self.timer = self.create_timer(1.0 / rate, self.step)

        # per-leg IK constants
        self.home = {}
        for nm in self.leg_names:
            L = self.legs[nm]
            fx0, fy0, fz0 = L["foot_home"]          # foot home, relative to hip
            self.home[nm] = {
                "fx0": fx0,
                "fy0": fy0,
                "fz0": fz0,
                "dir": math.atan2(fy0, fx0),        # home leg direction
                "L1": L["L1"],
                "L2": L["L2"],
                "cp": L["coxa_pitch"],              # coxa pitch (fixed)
            }

        self.get_logger().info(
            f"gait node started: stride={self.stride} lift={self.lift} speed={self.speed}"
        )

    def ik(self, nm, phase):
        h = self.home[nm]
        # foot target relative to hip: swing forward/back in +X, fixed Y, lift in Z
        fx = h["fx0"] + self.stride * math.cos(phase)
        fy = h["fy0"]
        fz = h["fz0"] + self.lift * max(0.0, -math.sin(phase))

        # hip yaw = change of the leg direction in the XY plane (normalised)
        hip = math.atan2(fy, fx) - h["dir"]
        hip = math.atan2(math.sin(hip), math.cos(hip))

        # knee pitch: 2-link IK in the leg plane (coxa fixed pitch + femur)
        d = math.hypot(fx, fy)
        kx = h["L1"] * math.cos(h["cp"])
        kz = h["L1"] * math.sin(h["cp"])
        femur_ang = math.atan2(fz - kz, d - kx)
        knee = femur_ang - h["cp"]

        ankle = 0.0
        return hip, knee, ankle

    def step(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names

        positions = []
        dt = 1.0 / self.get_parameter("rate").value
        for nm in self.leg_names:
            self.phase[nm] += self.speed * dt
            if self.phase[nm] > 2 * math.pi:
                self.phase[nm] -= 2 * math.pi
            hip, knee, ankle = self.ik(nm, self.phase[nm])
            positions += [hip, knee, ankle]
        msg.position = positions

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GaitNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

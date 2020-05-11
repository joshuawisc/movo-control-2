#!/usr/bin/python

import rospy
from geometry_msgs.msg import PoseStamped, Vector3Stamped, QuaternionStamped, Pose
from movo_msgs.msg import GripperCmd
from std_msgs.msg import Bool
from relaxed_ik.msg import EEPoseGoals
import RelaxedIK.Utils.transformations as T
from inputs import get_gamepad
import sys
import multiprocessing
import time
import os, signal
from movo_mimicry.msg import XboxInputs

# ---
# Takes Xbox controller inputs from ROS topics
# Publishes bimanual movement information for the Movo
# ---


rospy.init_node('xbox_driver')

position_r = [0.,0.,0.]
rotation_r = [1.,0.,0.,0.]

position_l = [0.,0.,0.]
rotation_l = [1.,0.,0.,0.]

pos_step = 0.001
rot_step = 0.005
pos_add_r = [0.,0.,0.]

inputs = [0] * 19
stick_limit = 17000

def xbox_cb(data):
    global inputs
    inputs = data.inputs

def grab_l(val):
    cmd = GripperCmd()
    cmd.position = val  # 0 - 0.9
    cmd.speed = 0.5
    gripper_pub_l.publish(cmd)

ee_pose_goals_pub = rospy.Publisher('/relaxed_ik/ee_pose_goals', EEPoseGoals, queue_size=5)
xbox_outputs_sub = rospy.Subscriber('/xbox_inputs', XboxInputs, xbox_cb)
gripper_pub_l = rospy.Publisher('/movo/left_gripper/cmd', GripperCmd, queue_size=10)

r = rospy.Rate(50)
while not rospy.is_shutdown():


    grab_l(inputs[2])

    ## left stick - left arm y
    if inputs[0] > stick_limit:
        position_l[1] -= pos_step
    elif inputs[0] < -1*stick_limit:
        position_l[1] += pos_step

    ## left stick - left arm x
    if inputs[1] > stick_limit:
        position_l[0] -= pos_step
    elif inputs[1] < -1*stick_limit:
        position_l[0] += pos_step

    ## left button - left arm up
    if inputs[12] == 1:
        position_l[2] += pos_step

    ## left trigger - left arm down
    if inputs[13] > 700:
        position_l[2] -= pos_step

    ## Dpad left/right- left arm rotation left/right
    if inputs[6] > 0:
        euler = list(T.euler_from_quaternion(rotation_l))
        euler[2] -= rot_step
        rotation_l = T.quaternion_from_euler(euler[0], euler[1], euler[2])
    elif inputs[6] < 0:
        euler = list(T.euler_from_quaternion(rotation_l))
        euler[2] += rot_step
        rotation_l = T.quaternion_from_euler(euler[0], euler[1], euler[2])

    ## Dpad up/down - left arm rotation up/down
    if inputs[7] > 0:
        euler = list(T.euler_from_quaternion(rotation_l))
        euler[1] += rot_step
        rotation_l = T.quaternion_from_euler(euler[0], euler[1], euler[2])
    elif inputs[7] < 0:
        euler = list(T.euler_from_quaternion(rotation_l))
        euler[1] -= rot_step
        rotation_l = T.quaternion_from_euler(euler[0], euler[1], euler[2])

    ## right stick - right arm y
    if inputs[3] > stick_limit:
        position_r[1] -= pos_step
    elif inputs[3] < -1*stick_limit:
        position_r[1] += pos_step

    ## right stick - right arm x
    if inputs[4] > stick_limit:
        position_r[0] -= pos_step
    elif inputs[4] < -1*stick_limit:
        position_r[0] += pos_step

    ## right button - right arm up
    if inputs[14] == 1:
        position_r[2] += pos_step

    ## right trigger - right arm down
    if inputs[15] > 700:
        position_r[2] -= pos_step

    ## X/B Button - right arm rotation
    if inputs[8] > 0:
        euler = list(T.euler_from_quaternion(rotation_r))
        euler[2] += rot_step
        rotation_r = T.quaternion_from_euler(euler[0], euler[1], euler[2])
    if inputs[10] > 0:
        euler = list(T.euler_from_quaternion(rotation_r))
        euler[2] -= rot_step
        rotation_r = T.quaternion_from_euler(euler[0], euler[1], euler[2])

    ## Y/A - right arm rotation
    if inputs[11] > 0:
        euler = list(T.euler_from_quaternion(rotation_r))
        euler[1] -= rot_step
        rotation_r = T.quaternion_from_euler(euler[0], euler[1], euler[2])
    if inputs[9] > 0:
        euler = list(T.euler_from_quaternion(rotation_r))
        euler[1] += rot_step
        rotation_r = T.quaternion_from_euler(euler[0], euler[1], euler[2])

    ee_pose_goals = EEPoseGoals()
    pose_r = Pose()
    pose_r.position.x = position_r[0]
    pose_r.position.y = position_r[1]
    pose_r.position.z = position_r[2]

    pose_r.orientation.w = rotation_r[0]
    pose_r.orientation.x = rotation_r[1]
    pose_r.orientation.y = rotation_r[2]
    pose_r.orientation.z = rotation_r[3]

    pose_l = Pose()
    pose_l.position.x = position_l[0]
    pose_l.position.y = position_l[1]
    pose_l.position.z = position_l[2]

    pose_l.orientation.w = rotation_l[0]
    pose_l.orientation.x = rotation_l[1]
    pose_l.orientation.y = rotation_l[2]
    pose_l.orientation.z = rotation_l[3]
    ee_pose_goals.ee_poses.append(pose_r)
    ee_pose_goals.ee_poses.append(pose_l)
    # print(pose_r)
    ee_pose_goals_pub.publish(ee_pose_goals)

    r.sleep()



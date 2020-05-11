# Movo Mimicry Control ROS Package

# Contents
1. Files Included
2. Requirements
3. Setup
4. Mimicry Control
    1. Requirements
    2. Setup
    3. Usage
5. Xbox Control
6. Latency System

# 1. Files included

* movo_mimicry - Movo mimicry control ROS package
    * Movo velocity control node
    * Movo xbox control files
    * Movo latency system files
    * Movo mimicry control files
* Config - Movo RelaxedIK Config files
* controller_publisher_dual.py - Mimicry control file

# 2. Requirements
* RelaxedIK [link]
* mimicry_control ROS package
* Movo description [link]

# 3. Setup
* Setup RelaxedIK with Movo using given Config file
* Add *controller_publisher_dual.py* into mimicry_control/src/bin

# 4. Mimicry Control

## Usage

Connect an ethernet cable from the back of the 
Movo to the Windows machine

### Linux (ROS):

Run / Launch the following ROS nodes -

movo_mimicry.launch : for 2 Vive controllers  
OR
movo_mimicry_single.launch : for 1 Vive controller


### Windows (Unity):
1. Open vive-teleop-movo project
2. Set IP on broadcaster game object to 10.66.171.1
3. Make sure one or both controllers are on and connected
4. Click play

# 5. Xbox Control

## Usage

Run / Launch the following ROS nodes -

#### RelaxedIK nodes
* load_info_file.py
* relaxed_ik_julia.launch

#### Mimicry Control nodes
* xbox_control.py (movo_mimicry):
* xbox_to_ros.py (movo_mimicry):
* movo_vel_controller.py (movo_mimicry): Sends relaxedIK solutions to Movo arm controllers

# 6. Latency System

## Usage

Run / Launch the following ROS nodes -

#### RelaxedIK nodes
* load_info_file.py
* relaxed_ik_julia.launch

#### Mimicry Control nodes
* movo_latency.launch
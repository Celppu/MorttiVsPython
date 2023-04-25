from multiprocessing import Process, Array
import pybullet as p
import time
import pybullet_data

def main(joint_angles):
    robot = setup_pybullet()

    while True:
        set_joint_angles(robot, joint_angles[:])
        p.stepSimulation()
        time.sleep(1.0 / 240.0)
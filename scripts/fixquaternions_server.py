#!/usr/bin/env python3
#http://wiki.ros.org/tf/Tutorials/Writing%20a%20tf%20listener%20%28Python%29

import rospy
#import math
from numpy.linalg import norm
from dynamic_reconfigure.server import Server
from gait1992_description.cfg import FixPoseConfig
import tf
from geometry_msgs.msg import Quaternion
import sys

def callback(config, level):
    rospy.loginfo("""Reconfigure Request:
            r:{roll}, p:{pitch}, y:{yaw},\ 
            {use_q},\ 
            {qx}, {qy}, {qz}, {qw},\ 
            {origin_x}, {origin_y}, {origin_z},\ 
            """.format(**config))
    # normalize quaternion
    q = [config["qx"],config["qy"],config["qz"],config["qw"]]
    noo = float(norm(q))
    print(noo)
    qq = Quaternion()
    qq.x = config["qx"]/noo 
    qq.y = config["qy"]/noo 
    qq.z = config["qz"]/noo 
    qq.w = config["qw"]/noo 
    
    #TODO:I should also try to generate the rpy and so back, but, not now.
    if config["use_q"]:
        #set rpy from quaternions
        # help says the order is sxyz , so I don't know. trying all combinations
        angles = tf.transformations.euler_from_quaternion([qq.x, qq.y, qq.z, qq.w])
        config["roll"] = angles[0]
        config["pitch"] = angles[1]
        config["yaw"] = angles[2]
    else:
        ## okay, roll pitch and yaw and Euler angles are different things, this is likely not going to work from the get-go
        q_rot = tf.transformations.quaternion_from_euler(config["roll"], config["pitch"], config["yaw"])
        qq.x = float(q_rot[0])
        qq.y = float(q_rot[1])
        qq.z = float(q_rot[2])
        qq.w = float(q_rot[3])
    #raise()

    config["qx"] = qq.x
    config["qy"] = qq.y
    config["qz"] = qq.z
    config["qw"] = qq.w
    print(config)
    return config

if __name__ == '__main__':
    try:
        #This is only necessary if this is being called with rosrun. then I need to make sure I setup a reasonable name for the node because dynamic_reconfigure 
        # looks for server based on node names. Its weird, I know, yet another way of sending info
        if len(sys.argv) == 1:
            node_name = "ximu3"
        else:
            node_name = sys.argv[1]
        effective_server_name =node_name + '_pose_publisher_updater' 
        rospy.init_node( node_name + '_pose_publisher_updater')
        rospy.loginfo("Waiting for dynamic_reconfigure calls at: %s"%rospy.get_name())

        srv = Server(FixPoseConfig, callback)
        rospy.spin()
    except rospy.ROSException as e:
        rospy,logerr("something wrong happened %s"%e)
        


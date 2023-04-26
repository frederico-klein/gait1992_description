#!/usr/bin/env python3

import rospy
import tf
import std_msgs.msg
from dynamic_reconfigure.client import Client
from gait1992_description.cfg import FixPoseConfig

class FloatingJointStatePublisher:

    def __init__(self, parent="map", child="ximu3"):
        self.r = 0 
        self.p = 0
        self.y = 0
        self.qx = 0
        self.qy = 0
        self.qz = 0
        self.qw = 1
        self.origin_x = 0
        self.origin_y = 0
        self.origin_z = 0
        self.child_frame_id = rospy.get_param("~child_frame_id",child)
        self.pose_server_node_name = rospy.get_param("~pose_publisher_name",self.child_frame_id + "_pose_publisher_updater")
        self.parent_frame_id = rospy.get_param("~parent_frame_id",parent)
        self.use_quaternions = False

    def callback(self, config):
        rospy.loginfo("""Reconfigure Request:
            r:{roll}, p:{pitch}, y:{yaw},\ 
            {use_q},\ 
            {qx}, {qy}, {qz}, {qw},\ 
            {origin_x}, {origin_y}, {origin_z},\ 
            """.format(**config))

        self.r = config["roll"]
        self.p = config["pitch"]
        self.y = config["yaw"]

        self.qx = config["qx"]
        self.qy = config["qy"]
        self.qz = config["qz"]
        self.qw = config["qw"]

        self.origin_x = config["origin_x"]
        self.origin_y = config["origin_y"]
        self.origin_z = config["origin_z"]

        self.use_quaternions = config["use_q"]
        return config

    def publisher(self):

        #pub = rospy.Publisher('pose', PoseStamped, queue_size=1)
        listener = tf.TransformListener()
        rate = rospy.Rate(10) # Hz
        h = std_msgs.msg.Header()
        h.frame_id = self.parent_frame_id
        br = tf.TransformBroadcaster()
        rospy.loginfo("trying to connect to dynamic_reconfigure server: %s"%self.pose_server_node_name)
        cl = Client(self.pose_server_node_name, 30, self.callback)

        while not rospy.is_shutdown():
            if self.use_quaternions:
                q_rot = [self.qx,self.qy,self.qz,self.qw]
            else:
                q_rot = tf.transformations.quaternion_from_euler(self.r, self.p, self.y);

            #br.sendTransform((0.5, 0.5, 0), (0,0,0,1), rospy.Time.now(), self.new_frame_id+"_transl", self.parent_frame_id)
            origin = (self.origin_x,self.origin_y,self.origin_z)
            br.sendTransform(origin, q_rot, rospy.Time.now(), self.child_frame_id, self.parent_frame_id)

            rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('pose_publisher', anonymous=True)
        a = FloatingJointStatePublisher(child="ximu3", parent="map")
        a.publisher()
    except (rospy.ROSException, rospy.ServiceException) as e:
        rospy.logerr("Something failed. %s"%e)
        


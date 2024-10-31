#!/usr/bin/env python3

###TODO: this is a bit harder than anticipated
# right now it is almost correct, I think, but there is a pelvis heading angle which is unaccounted for, 
# since the imus are showing orientations relative to map, we actually need a TF here to measure the pelvis 
# initial orientation and subtract it. if we change it in the URDF it will work, but everything else will break, 
# so we need to flip them here, I think.
# still unsure. 
# if a heading correction is all we need, we can do it here, BUT we are going to have yet another set of global coordinates
# to keep track of, and it is getting confusing. 

import rospy
import csv
import shutil
import re
#read a calibrated file and generate all /tmp/imu_calibrated/.yaml files

#read the calibration file and create a class

class Quaternion:
    def __init__(self, x=0,y=0,z=0,w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.conv_dic_1 = {1:"x",2:"y",3:"z",4:"w",}
        self.conv_dic_2 = {1:"w",2:"x",3:"y",4:"z",}

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "x:{},y:{},z:{},w:{}".format(self.x, self.y, self.z, self.w)

    def get(self, axis):
        if axis == "x":
            return self.x
        if axis == "y":
            return self.y
        if axis == "z":
            return self.z
        if axis == "w":
            return self.w

    def set_by_num(self, num,val):
        val = float(val)
        conv_dic = self.conv_dic_2
        if conv_dic[num] == "x":
            self.x = str(val)
        if conv_dic[num] == "y":
            self.y = str(val)
        if conv_dic[num] == "z":
            self.z = str(val)
        if conv_dic[num] == "w":
            self.w = str(-val)

class CalibratedImuData:
    def __init__(self, filename, imu_defaults_dir):
        self.filename = filename
        self.imu_defaults_dir = imu_defaults_dir
        self.orientation_dict = {}
        self.update_orientation_dict()

    def update_orientation_dict(self):
        ## opens file
        with open(self.filename, "r") as csvfile:
            line = ""
            while "endheader" not in line:
                line = csvfile.readline()
            reader = csv.DictReader(csvfile, delimiter="\t")
            row_dic = next(reader)
            list_of_imus = []
            for name in row_dic.keys():
                p_name = name.rsplit("_",1)
                if p_name[0] not in list_of_imus and "q" in p_name[-1]:
                    list_of_imus.append(p_name[0])
            print(list_of_imus)
            for imu_name in list_of_imus:
                ## iterates over columns and builds a list with
                #imu_name = "some_name"
                ori = Quaternion()
                for i in range(1,5):
                    ori.set_by_num(i,row_dic["{}_q{}".format(imu_name,i)])
                this_imu_dict = {imu_name:ori}
                self.orientation_dict.update(this_imu_dict)
        print(self.orientation_dict)

    def create_tmp_calib(self):
        """ 
        creates files in /tmp
        """
        ##creates the directory if it doesnt exist
        ##iterates over imus in orientation dict
        shutil.copytree(self.imu_defaults_dir,"/tmp/imu_calib")
        for imu_name, q in self.orientation_dict.items():
            print(imu_name,q)
            new_file = "/tmp/imu_calib/{}.yaml".format(imu_name)
            #copies file over to /tmp/something
            #print(ori_file)
            with open(new_file, "r+") as f:
                text = f.read()
                    #print(row)
                text = re.sub("use_q: false", "use_q: true", text)
                for i, letter in enumerate(["x","y","z","w"]):
                    r ="(q{}:).*".format(letter) 
                    new_str = "\\1 {}".format(q.get(letter))
                    print(new_str)
                    text = re.sub(r,new_str,text)
                        #print(q)
                        #print(q.get(letter))
                        #print("DDDDDDDDDDDDDDDDDDDDDDDDDDDD %s"%m.group(0))
                    #print(row)
            with open(new_file, "w") as f:
                f.write(text)
            #regexes the stuff from q? to be what it is from 
            
if __name__ == '__main__':
    try:
        #rospy.init_node('calibrator_reader', anonymous=True)
        #a = CalibratedImuData("/tmp/2023-03-06-13-14-07walking011calib.sto","/catkin_ws/src/gait1992_description/imu_defaults/")
        a = CalibratedImuData("/tmp/2023-03-03-12-13-11ssss0113calib.sto","/catkin_ws/src/gait1992_description/imu_defaults/")
        a.create_tmp_calib()
    except rospy.ROSException as e:
        rospy.logerr("Something failed. %s"%e)
        


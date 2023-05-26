#!/usr/bin/env bash
set -e

tmux new-session -s imu_fixing -d 
tmux set-option -s -t imu_fixing default-command "bash --rcfile ~/.bashrc_ws.sh"
tmux send -t imu_fixing:0.0 "roscore" C-m
sleep 2

tmux new-window
tmux select-window -t 1
tmux split-window -h 
tmux split-window -h 
tmux split-window -h 
tmux select-layout even-horizontal
tmux select-pane -t 3
tmux split-window -v -p 50 
tmux select-pane -t 2
tmux split-window -v -p 50 
tmux select-pane -t 1 
tmux split-window -v -p 50 
tmux select-pane -t 0
tmux split-window -v -p 50 

tmux new-window
tmux select-window -t 2
tmux split-window -h 
tmux split-window -h 
tmux split-window -h 
tmux select-layout even-horizontal
tmux select-pane -t 3
tmux split-window -v -p 50 
tmux select-pane -t 2
tmux split-window -v -p 50 
tmux select-pane -t 1 
tmux split-window -v -p 50 
tmux select-pane -t 0
tmux split-window -v -p 50 
#tmux select-layout tiled
#tmux select-pane -t 0

#sends keys to first and second terminals
#tmux send -t imu_fixing:1.0 "rviz -d /catkin_ws/_cam_tf.rviz" C-m
 #rviz -d ./_default.rviz
tmux send -t imu_fixing:1.0 "roslaunch gait1992_description human_control_imus_movable.launch" C-m
tmux send -t imu_fixing:1.1 "rosrun rqt_reconfigure rqt_reconfigure" C-m
tmux send -t imu_fixing:1.2 "rosrun gait1992_description fixheading_server.py" C-m
#tmux send -t imu_fixing:1.3 "rosrun rqt_reconfigure rqt_reconfigure" C-m
#tmux send -t imu_fixing:1.4 "rosservice call /inverse_kinematics_from_file/start" C-m
#tmux send -t imu_fixing:1.5 "roslaunch opensimrt	id.launch" C-m
#tmux send -t imu_fixing:1.6 "ls -la" C-m

tmux send -t imu_fixing:2.0 "roslaunch gait1992_description imu_initial_pose_setter.launch body:=torso" C-m
tmux send -t imu_fixing:2.1 "roslaunch gait1992_description imu_initial_pose_setter.launch body:=pelvis" C-m
tmux send -t imu_fixing:2.2 "roslaunch gait1992_description imu_initial_pose_setter.launch body:=femur_l" C-m
tmux send -t imu_fixing:2.3 "roslaunch gait1992_description imu_initial_pose_setter.launch body:=femur_r" C-m
tmux send -t imu_fixing:2.4 "roslaunch gait1992_description imu_initial_pose_setter.launch body:=tibia_l" C-m
tmux send -t imu_fixing:2.5 "roslaunch gait1992_description imu_initial_pose_setter.launch body:=tibia_r" C-m
tmux send -t imu_fixing:2.6 "roslaunch gait1992_description imu_initial_pose_setter.launch body:=talus_l" C-m
tmux send -t imu_fixing:2.7 "roslaunch gait1992_description imu_initial_pose_setter.launch body:=talus_r" C-m

#tmux setw synchronize-panes on

tmux -2 a -t imu_fixing

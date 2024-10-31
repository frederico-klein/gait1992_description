#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from acquisition_fb_flexbe_states.variable_tmux_setup_from_yaml_state import VariableTmuxSetupFromYamlState
from flexbe_states.log_state import LogState
from gait1992_fb_flexbe_states.env_vars_userdata_setter import UrdfEnvUserDataSetterState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]
import rospkg
# [/MANUAL_IMPORT]


'''
Created on Thu Oct 31 2024
@author: fbk
'''
class urdf_simple_scalingSM(Behavior):
	'''
	attempt as scaling by height
	'''


	def __init__(self):
		super(urdf_simple_scalingSM, self).__init__()
		self.name = 'urdf_simple_scaling'

		# parameters of this behavior
		self.add_parameter('model_flexbe_package', 'gait1992_fb_flexbe_behaviors')
		self.add_parameter('height', 1.8)
		self.add_parameter('tf_prefix', 'ik')
		self.add_parameter('foot_distance_from_ground', 0)
		self.add_parameter('ignore_insole_imu_for_vis', True)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		self.rospack = rospkg.RosPack()
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		package_path = self.find_pkg(self.model_flexbe_package)
		session_name = "testtt"
		config_file = package_path+"/config/urdf_everything.yaml"
		# x:30 y:365, x:920 y:670
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.load_env = {}
		_state_machine.userdata.tf_prefix = self.tf_prefix
		_state_machine.userdata.foot_left_name = "calcn_l"
		_state_machine.userdata.foot_right_name = "calcn_r"
		_state_machine.userdata.foot_distance_from_ground = self.foot_distance_from_ground
		_state_machine.userdata.ignore_insole_imu_for_vis = self.ignore_insole_imu_for_vis
		_state_machine.userdata.node_start_list = []
		_state_machine.userdata.use_gui = False
		_state_machine.userdata.base_parent = "map"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:204 y:28
			OperatableStateMachine.add('find_model_package',
										LogState(text=package_path, severity=Logger.REPORT_HINT),
										transitions={'done': 'urdf_vars_setter'},
										autonomy={'done': Autonomy.Off})

			# x:766 y:246
			OperatableStateMachine.add('node_loader',
										VariableTmuxSetupFromYamlState(session_name=session_name, startup_yaml=config_file, append_node=[]),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Full, 'failed': Autonomy.High},
										remapping={'node_start_list': 'node_start_list', 'load_env': 'load_env'})

			# x:386 y:465
			OperatableStateMachine.add('urdf_vars_setter',
										UrdfEnvUserDataSetterState(),
										transitions={'done': 'node_loader'},
										autonomy={'done': Autonomy.Off},
										remapping={'use_gui': 'use_gui', 'base_parent': 'base_parent', 'tf_prefix': 'tf_prefix', 'foot_left_name': 'foot_left_name', 'foot_right_name': 'foot_right_name', 'foot_distance_from_ground': 'foot_distance_from_ground', 'ignore_insole_imu_for_vis': 'ignore_insole_imu_for_vis', 'env_vars': 'load_env'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	def find_pkg(self, pkg):
		return self.rospack.get_path(pkg)
	
	# [/MANUAL_FUNC]

#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]
import rospkg
# [/MANUAL_IMPORT]


'''
Created on Thu Oct 31 2024
@author: fbk
'''
class test_functionSM(Behavior):
	'''
	tests usage of private function to find package. 

open the source code and copy paste it to use in your own behavior
	'''


	def __init__(self):
		super(test_functionSM, self).__init__()
		self.name = 'test_function'

		# parameters of this behavior
		self.add_parameter('height', 0)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		self.rospack = rospkg.RosPack()
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		hello = self.find_pkg("gait1992_description")
		# x:30 y:365, x:457 y:431
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:359 y:151
			OperatableStateMachine.add('test_log',
										LogState(text=hello, severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	def find_pkg(self, pkg):
		return self.rospack.get_path(pkg)
	# [/MANUAL_FUNC]

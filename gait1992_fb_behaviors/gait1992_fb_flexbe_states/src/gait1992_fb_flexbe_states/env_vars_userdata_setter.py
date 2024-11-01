#!/usr/bin/env python

from flexbe_core import EventState, Logger
import traceback
'''
Created on 14-Feb-2018

@author: David Conner
'''

class UrdfEnvUserDataSetterState(EventState):
    '''
    Implements a state that defines user data

    #< use_gui             desc
    #< should_load_ar      desc
    #< env_vars            initial env_vars (in case you already have set some stuff)
    #> env_vars            The generated user_vars

    <= done                Created the user data
    '''


    def __init__(self ):
        '''
        Constructor
        '''
        super(UrdfEnvUserDataSetterState, self).__init__(input_keys=["scale","use_gui","base_parent","tf_prefix","foot_left_name","foot_right_name","insole_distance_from_foot","insole_length", "ignore_insole_imu_for_vis","adjustable_tfs","env_vars"], output_keys=["env_vars"], outcomes=["done"])

        self._return_code = None

    def execute(self, userdata):
        '''
        Execute this state
        '''
        return self._return_code


    def on_enter(self, userdata):

        try:

          # Add the user data
          userdata.env_vars.update(  {
              "USE_GUI"                     : userdata.use_gui                          ,
              "BASE_PARENT"                 : userdata.base_parent                      ,
              "TF_PREFIX"                   : userdata.tf_prefix                        ,
              "FOOT_RIGHT_NAME"             : userdata.foot_right_name                  ,
              "FOOT_LEFT_NAME"              : userdata.foot_left_name                   ,
              "INSOLE_LENGTH"               : userdata.insole_length                    ,
              "INSOLE_DISTANCE_FROM_FOOT"   : userdata.insole_distance_from_foot               ,
              "IGNORE_INSOLE_IMU_FOR_VIS"   : userdata.ignore_insole_imu_for_vis        ,
              "ADJUSTABLE_TFS"              : userdata.adjustable_tfs                   ,
              "SCALE"                       : userdata.scale                            ,
              })
          Logger.logdebug(f"[env_vars_userdata_setter] env_vars:  {userdata.env_vars}")
          self._return_code = 'done'
        except:
            traceback.print_exc()
            raise ValueError('UserDataState %s - invalid data ' % self.name)

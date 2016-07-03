#!/usr/bin/env python
#
#  Copyright (c) 2015 MIT. All rights reserved.
#
#   author: Pedro Santana
#   e-mail: psantana@mit.edu
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#  3. Neither the name(s) of the copyright holders nor the names of its
#     contributors or of the Massachusetts Institute of Technology may be
#     used to endorse or promote products derived from this software
#     without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
#  AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
"""
RAO*: a risk-aware planner for POMDP's.

Demo showing the integration between pSulu and RAO* through RMPyL.

@author: Pedro Santana (psantana@mit.edu).
"""
from pysulu.psulu_rmpyl import PySuluRMPyL
from rao.models.psulu import pSuluRockSampleModel
from rao.raostar import RAOStar
from rao.export import policy_to_dot,policy_to_rmpyl
import pickle

#Sets up pSulu according to pysulu_config.txt
psulu = PySuluRMPyL()

# sites={'minerals':{'coords':(0.0,-10.0),'value':10.0},
#        'funny_rock':{'coords':(-10.0,-10.0),'value':5.0},
#        'boulder_shadow':{'coords':(-13.0,0.0),'value':3.0},
#        'geiser':{'coords':(0.0,10.0),'value':4.0},
#        'alien_lair':{'coords':(13.0,13.0),'value':100.0}}
#
# prior={'minerals':0.5,
#        'funny_rock':0.5,
#        'boulder_shadow':0.5,
#        'geiser':0.5,
#        'alien_lair':0.2}

sites={'minerals':{'coords':(0.0,-10.0),'value':10.0},
       'funny_rock':{'coords':(-10.0,-10.0),'value':5.0},
       'geiser':{'coords':(0.0,10.0),'value':4.0},
       'alien_lair':{'coords':(13.0,13.0),'value':100.0}}

prior={'minerals':0.5,
       'funny_rock':0.5,
       'geiser':0.5,
       'alien_lair':0.2}

# sites={'minerals':{'coords':(0.0,-10.0),'value':10.0},
#        'funny_rock':{'coords':(-10.0,-10.0),'value':5.0},
#        'alien_lair':{'coords':(13.0,13.0),'value':100.0}}
#
# prior={'minerals':0.5,
#        'funny_rock':0.3,
#        'alien_lair':0.2}

# sites={'minerals':{'coords':(0.0,-10.0),'value':10.0}}
# prior={'minerals':0.3}

# parameters = {}
# parameters['executor']='ProOFCSA'    #Solving algorithm
# parameters['chance_constraint']=0.01 #Maximum allowed risk
# parameters['std-position']=0.1       #Initial position uncertainty
# parameters['std-velocity']=0.0       #Initial velocity uncertainty
# parameters['inc-factor']=0.5         #Uncertainty increase rate (1.0 means 100% growth by the end of the route)
# parameters['waypoints']=10           #Number of waypoints from start to goal
# parameters['time_horizon']=200.0     #Time horizon for the route (in seconds)
# parameters['max-velocity']=0.4       #Agent's maximum velocity (in m/s)
# parameters['save png']=0             #Save map to file

initial_pos = (-12.5,13.5)

cc_pp = pSuluRockSampleModel(path_planner=psulu,sites=sites,duration_type='uniform',verbose=0)

b0 = cc_pp.get_initial_belief(initial_pos=initial_pos,prior=prior)

cc_pp.load_cached_paths('mars_rover_paths.pickle')

planner = RAOStar(cc_pp,node_name='id',cc=0.01,cc_type='overall',
                  terminal_prob=1.0,randomization=0.0,propagate_risk=True,
                  expand_all_open=True,verbose=1)

policy,explicit,performance = planner.search(b0)

cc_pp.write_cached_paths('mars_rover_paths.pickle')

dot_policy = policy_to_dot(explicit,policy)
rmpyl_policy = policy_to_rmpyl(explicit,policy)

#Writes control program to pickle file
with open('rover_policy_rmpyl.pickle','wb') as f:
    pickle.dump(rmpyl_policy,f)

dot_policy.write('rover_psulu_policy.svg',format='svg')
rmpyl_policy.to_ptpn(filename='rover_psulu_policy_rmpyl_ptpn.tpn')

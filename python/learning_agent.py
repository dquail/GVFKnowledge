# Copyright 2016 Google Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""Basic random agent for DeepMind Lab."""

#Basic imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import argparse
import random
import numpy as np
import six
import time

#Project imports
from GVF import *
from BehaviorPolicy import *

#Deepmind import
import deepmind_lab

class LearningForeground:
  def __init__(self, length, width, height, fps, level, record, demo, video):

    #Set up our environment
    config = {
      'fps': str(fps),
      'width': str(width),
      'height': str(height)
    }
    if record:
      config['record'] = record
    if demo:
      config['demo'] = demo
    if video:
      config['video'] = video
    self.env = deepmind_lab.Lab(level, ['RGBD'], config=config)

    #Set our behavior policy
    self.behaviorPolicy = BehaviorPolicy()

    self.featureRepresentationLength = 100
    alpha = 0.1
    numberOfActiveFeatures = 5
    #Set up our GVF for pavlovian control
    gvf = GVF(self.featureRepresentationLength, alpha / numberOfActiveFeatures, isOffPolicy = False, name = "Hit wall GVF")
    gvf.gamma = 0
    gvf.policy = self.behaviorPolicy
    self.wallGVF = gvf

    #Set learning parameters
    self.previousObs = False
    self.currentObs = False

  def createFeatureRepresentation(self, observation, action):
    if observation == None:
      return None
    else:
      #TODO: tilecode the observation RGB bits.
      return np.zeros(self.featureRepresentationLength)

  def updateGVFs(self):
    print("TBD: GVF learning")
    gvf = self.wallGVF

  def start(self, numberOfSteps = 10000, numberOfRuns = 1):
    for run in range(numberOfRuns):
      print("RUN NUMBER: " + str(run + 1) + " ......")
      self.env.reset()
      self.lastAction = 0
      self.currentAction = 0
      self.previousObs = False

      for step in range(numberOfSteps):
        #TODO - make this a pavlovian prediction
        willHitWall = False

        #Pavlovian control
        action = None
        if willHitWall == True:
          action = self.behaviorPolicy.turnLeftPolicy(self.previousObs)
        else:
          action = self.behaviorPolicy.policy(self.previousObs)
        self.currentAction = action
        if self.currentObs:
          self.previousObs = self.currentObs

        print("Action:")
        print(action)
        reward = self.env.step(action, num_steps=1)
        self.currentObs = self.env.observations()
        #Learn
        self.updateGVFs()



def run(length, width, height, fps, level, record, demo, video):
  """Spins up an environment and runs the random agent."""
  config = {
      'fps': str(fps),
      'width': str(width),
      'height': str(height)
  }
  if record:
    config['record'] = record
  if demo:
    config['demo'] = demo
  if video:
    config['video'] = video
  #env = deepmind_lab.Lab(level, ['RGB_INTERLEAVED'], config=config)
  env = deepmind_lab.Lab(level, ['RGBD'], config=config)


  env.reset()

  # Starts the random spring agent. As a simpler alternative, we could also
  # use DiscretizedRandomAgent().

  #Spring is more based on smooth physics
  #agent = SpringAgent(env.action_spec())

  #Discretized is more jarring but simpler.
  agent = DiscretizedRandomAgent()

  reward = 0

  i = 0
  for _ in six.moves.range(length):
    if not env.is_running():
      print('Environment stopped early')
      env.reset()
      agent.reset()
    obs = env.observations()
    #action = agent.step(reward, obs['RGB_INTERLEAVED'])
    action = agent.step(reward, obs['RGBD'])
    reward = env.step(action, num_steps=1)
    i+=1
    time.sleep(1.0)
    print(i)

  print('Finished after %i steps. Total reward received is %f'
        % (length, agent.rewards))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--length', type=int, default=1000,
                      help='Number of steps to run the agent')
  parser.add_argument('--width', type=int, default=80,
                      help='Horizontal size of the observations')
  parser.add_argument('--height', type=int, default=80,
                      help='Vertical size of the observations')
  parser.add_argument('--fps', type=int, default=60,
                      help='Number of frames per second')
  parser.add_argument('--runfiles_path', type=str, default=None,
                      help='Set the runfiles path to find DeepMind Lab data')
  parser.add_argument('--level_script', type=str,
                      default='tests/empty_room_test',
                      help='The environment level script to load')
  parser.add_argument('--record', type=str, default=None,
                      help='Record the run to a demo file')
  parser.add_argument('--demo', type=str, default=None,
                      help='Play back a recorded demo file')
  parser.add_argument('--video', type=str, default=None,
                      help='Record the demo run as a video')

  args = parser.parse_args()
  if args.runfiles_path:
    deepmind_lab.set_runfiles_path(args.runfiles_path)

  foreground = LearningForeground(args.length, args.width, args.height, args.fps, args.level_script,
      args.record, args.demo, args.video)
  foreground.start(numberOfSteps = args.length, numberOfRuns = 1)

  """
  run(args.length, args.width, args.height, args.fps, args.level_script,
      args.record, args.demo, args.video)
  """
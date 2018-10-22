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

# Basic imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import random
import numpy as np
import six
import time
from matplotlib import pyplot as PLT

# Project imports
from GVF import *
from BehaviorPolicy import *
from StateRepresentation import *

# Deepmind import
import deepmind_lab

def didBumpCumulant(phi):
  return phi[len(phi) - 1]

def didBumpGamma(phi):
  return 0

class LearningForeground:
  def __init__(self, length, width, height, fps, level, record, demo, video):

    # Set up our environment
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
    self.env = deepmind_lab.Lab(level, [OBS_KEY], config=config)
    self.env.reset()

    # Set our behavior policy
    self.behaviorPolicy = BehaviorPolicy()

    #Set up our wall gvf
    #    def __init__(self, featureVectorLength, alpha, isOffPolicy, name = "GVF name"):
    self.wallGVF = GVF(TOTAL_FEATURE_LENGTH, alpha = 0.2 /( NUM_IMAGE_TILINGS * NUM_RANDOM_POINTS), isOffPolicy=True, name="WallGVF")

    self.wallGVF.cumulant = didBumpCumulant
    self.wallGVF.policy = self.behaviorPolicy.moveForwardPolicy
    self.wallGVF.gamma = didBumpGamma

    # Set learning parameters
    self.previousObs = False
    self.currentObs = False

    self.stateRepresentation = StateRepresentation()


  def updateGVFs(self):
    #def learn(self, lastState, action, newState):
    self.wallGVF.learn(lastState = self.previousPhi, action = self.currentAction, newState = self.currentPhi)

  def start(self, numberOfSteps=10000, numberOfRuns=1):
    for run in range(numberOfRuns):
      print("RUN NUMBER: " + str(run + 1) + " ......")
      self.env.reset()
      self.lastAction = 0
      self.currentAction = 0
      self.previousObs = False
      self.previousPhi = self.stateRepresentation.getEmptyPhi()
      self.currentPhi = self.stateRepresentation.getEmptyPhi()

      hasPreviousObs = False

      willHitWall = False
      for step in range(numberOfSteps):
        #Pavlovian control
        action = None
        if willHitWall == True:
          time.sleep(3)
          print("Predicted to hit wall")
          action = self.behaviorPolicy.turnLeftPolicy(self.previousPhi)
        else:
          if hasPreviousObs:
            action = self.behaviorPolicy.policy(self.previousPhi)
          else:
            action = self.behaviorPolicy.moveForwardPolicy(self.previousPhi)

        self.currentAction = action

        reward = self.env.step(action, num_steps=1)

        # Observation, for RGBD, has 'shape': (180, 320, 4)} ie. env.observations[0][0] would return an array of 4 elements. a[R,G,B,D]

        self.previousObs = self.currentObs
        self.previousPhi = self.currentPhi

        self.currentObs = self.env.observations()
        self.currentPhi = self.stateRepresentation.getPhi(self.currentObs)

        if hasPreviousObs:
          # Learn
          #print("Prediction before: " + str(self.wallGVF.prediction(self.previousPhi)))
          self.updateGVFs()
          #print the prediction:
          #print("Prediction after: " + str(self.wallGVF.prediction(self.previousPhi)))
          newPrediction = self.wallGVF.prediction(self.currentPhi)
          willHitWall = newPrediction > WALL_THRESHOLD
          #print previous prediction if at wall now
          if (self.currentPhi[len(self.currentPhi) - 1] == 1):
            print("Prediction: " + str(self.wallGVF.prediction(self.previousPhi)))

        hasPreviousObs = True




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
  foreground.start(numberOfSteps=args.length, numberOfRuns=1)

  """
  run(args.length, args.width, args.height, args.fps, args.level_script,
      args.record, args.demo, args.video)
  """
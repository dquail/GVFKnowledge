from random import randint
import numpy as np

class BehaviorPolicy:




  def __init__(self):
    self.lastAction = 0
    self.i = 0

    self.ACTIONS = {
      'look_left': np.array([-50, 0, 0, 0, 0, 0, 0], dtype=np.intc),
      'look_right': np.array([50, 0, 0, 0, 0, 0, 0], dtype=np.intc),
      'forward': np.array([0, 0, 0, 1, 0, 0, 0], dtype=np.intc),
      'backward': np.array([0, 0, 0, -1, 0, 0, 0], dtype=np.intc),
      'fire': np.array([0, 0, 0, 0, 1, 0, 0], dtype=np.intc),
    }


  def policy(self, state):
    self.i = self.i + 1

    isFacingWall = state[len(state) - 1] == 1 #Last bit in the feature representation represents facing the wall
    if isFacingWall:
      return self.ACTIONS['look_left']
    else:
      return self.ACTIONS['forward']

  def randomPolicy(self, state):
    #TODO - Return random value
    return self.ACTIONS['look_left']

  def moveForwardPolicy(self, state):
    return self.ACTIONS['forward']

  def turnLeftPolicy(self, state):
    self.i = self.i + 1
    return self.ACTIONS['look_left']

  def epsilonGreedyPolicy(self, state):
    print("Do something here")

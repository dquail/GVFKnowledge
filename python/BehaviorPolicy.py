from random import randint
import numpy as np

class BehaviorPolicy:




  def __init__(self):
    self.lastAction = 0
    self.i = 0

    self.ACTIONS = {
      'look_left': np.array([-512, 0, 0, 0, 0, 0, 0], dtype=np.intc),
      'look_right': np.array([512, 0, 0, 0, 0, 0, 0], dtype=np.intc),
      'forward': np.array([0, 0, 0, 1, 0, 0, 0], dtype=np.intc),
      'backward': np.array([0, 0, 0, -1, 0, 0, 0], dtype=np.intc),
      'fire': np.array([0, 0, 0, 0, 1, 0, 0], dtype=np.intc),
    }


  def policy(self, state):
    self.i = self.i + 1
    #TODO - check to see if we are currently facing a wall. If so, turn left. Otherwise forward
    isFacingWall = False
    if isFacingWall:
      return self.ACTIONS['look_left']
    else:
      return self.ACTIONS['forward']

  def randomPolicy(self, state):
    #TODO - Return random value
    return self.ACTIONS['look_left']

  def moveForwardPolicy(self, state):
    self.lastAction = ACTIONS['forward']
    return self.ACTIONS['forward']

  def turnLeftPolicy(self, state):
    self.i = self.i + 1
    self.lastAction = self.ACTIONS['look_left']

    return self.ACTIONS['look_left']

  def epsilonGreedyPolicy(self, state):
    print("Do something here")

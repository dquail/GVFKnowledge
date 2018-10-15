"""
Various utility functions
"""

#import math
from StateRepresentation import *
from matplotlib import pyplot as PLT

def get_next_pow2(number):
    """ Gets the next highest power of two for number
    """
    return 2**int(math.ceil(math.log(number, 2)))

def showImageFrameFromObservation(observation):
  M = self.currentObs[OBS_KEY]
  PLT.imshow(M)
  PLT.show()

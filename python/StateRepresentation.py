#!/usr/bin/env python

"""Uses tilecoding to create state.

"""
import numpy as np
from tiles import *
import time

# image tiles
NUM_RANDOM_POINTS = 100
CHANNELS = 4
NUM_IMAGE_TILINGS = 4
NUM_IMAGE_INTERVALS = 4
SCALE_RGB = NUM_IMAGE_INTERVALS / 256.0

IMAGE_START_INDEX = 0

# constants relating to image size recieved
IMAGE_HEIGHT = 480  # rows
IMAGE_WIDTH = 640  # columns

NUMBER_OF_COLOR_CHANNELS = 3 #red, blue, green
PIXEL_FEATURE_LENGTH = np.power(NUM_IMAGE_INTERVALS, NUMBER_OF_COLOR_CHANNELS) * NUM_IMAGE_TILINGS
DID_BUMP_FEATURE_LENGTH = 1
TOTAL_FEATURE_LENGTH = PIXEL_FEATURE_LENGTH * NUM_RANDOM_POINTS + DID_BUMP_FEATURE_LENGTH
PIXEL_DISTANCE_CONSIDERED_BUMP = 230 #How close an object is in front of the avatar before it is considered to "bump" into it
# Channels
RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2
DEPTH_CHANNEL = 3
OBS_KEY = 'RGBD_INTERLEAVED'

WALL_THRESHOLD = 0.2 #If the prediction is greater than this, the pavlov agent will avert

class StateRepresentation(object):
  def __init__(self):
    self.pointsOfInterest = []
    self.numberOfTimesBumping = 0
    self.randomYs = np.random.choice(IMAGE_HEIGHT, NUM_RANDOM_POINTS, replace=False)
    self.randomXs = np.random.choice(IMAGE_WIDTH, NUM_RANDOM_POINTS, replace=False)

    for i in range(NUM_RANDOM_POINTS):
      point = self.randomXs[i], self.randomYs[i]
      self.pointsOfInterest.append(point)

  def didBump(self, observation):
    obs = observation[OBS_KEY]
    midPix = obs[IMAGE_WIDTH / 2, IMAGE_HEIGHT / 2]

    didBump = False
    depths = obs[:,:, DEPTH_CHANNEL]
    #closestPixel = np.amin(depths)
    closestPixel = midPix[DEPTH_CHANNEL]
    #print("Pixel: " + str(closestPixel))

    if  closestPixel < PIXEL_DISTANCE_CONSIDERED_BUMP:
      self.numberOfTimesBumping +=1
      didBump = True

    """
    if didBump:
      print("!!!!! BUMPED " + str(self.numberOfTimesBumping) + " time !!!!!")
      time.sleep(1.0)
    """
    return didBump

  def getEmptyPhi(self):
    return np.zeros(TOTAL_FEATURE_LENGTH)
  """
  Name: getPhi
  Description: Creates the feature representation (phi) for a given observation. The representation
    created by individually tile coding each NUM_RANDOM_POINTS rgb values together, and then assembling them. 
    Finally, the didBump value is added to the end of the representation. didBump is determined to be true if
    the closest pixel in view is less than PIXEL_DISTANCE_CONSIDERED_BUMP
  Input: the observation. This is the full pixel rgbd values for each of the IMAGE_WIDTH X IMAGE_HEIGHT pixels in view
  Output: The feature vector
  """
  def getPhi(self, observation):
    if not observation:
      return None
    rgbdObs = observation[OBS_KEY]
    #tilecode each pixel indivudually and then assemble

    phi = []

    for point in self.pointsOfInterest:
      #Get the pixel value at that point
      x = point[0]
      y = point[1]
      red = rgbdObs[y, x, RED_CHANNEL] / 256.0
      green = rgbdObs[y, x, GREEN_CHANNEL] / 256.0
      blue = rgbdObs[y, x, BLUE_CHANNEL] / 256.0

      pixelRep = np.zeros(PIXEL_FEATURE_LENGTH)
      #Tile code these 3 values together
      indexes = tiles(NUM_IMAGE_TILINGS, PIXEL_FEATURE_LENGTH, [red, green, blue])
      for index in indexes:
        pixelRep[index] = 1.0

      #Assemble with other pixels
      phi.extend(pixelRep)

    didBump = self.didBump(observation)
    phi.append(int(didBump))

    return np.array(phi)


#!/usr/bin/env python

"""Uses tilecoding to create state.

"""
import numpy as np
from tiles import *
import time

# image tiles
#NUM_RANDOM_POINTS = 100
NUM_RANDOM_POINTS = 2
CHANNELS = 4
NUM_IMAGE_TILINGS = 8
NUM_IMAGE_INTERVALS = 4
SCALE_RGB = NUM_IMAGE_INTERVALS / 256.0

IMAGE_START_INDEX = 0

# constants relating to image size recieved
"""
IMAGE_HEIGHT = 480  # rows
IMAGE_WIDTH = 640  # columns
"""
IMAGE_HEIGHT = 10  # rows
IMAGE_WIDTH = 10  # columns

NUMBER_OF_CHANNELS = 3 #red, blue, green
PIXEL_FEATURE_LENGTH = np.power(NUMBER_OF_CHANNELS, NUM_IMAGE_INTERVALS) * NUM_IMAGE_TILINGS
DID_BUMP_FEATURE_LENGTH = 0
TOTAL_FEATURE_LENGTH = PIXEL_FEATURE_LENGTH * NUM_RANDOM_POINTS + DID_BUMP_FEATURE_LENGTH

# Channels
RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2
DEPTH_CHANNEL = 3
OBS_KEY = 'RGBD_INTERLEAVED'

class StateRepresentation(object):
  def __init__(self):
    self.pointsOfInterest = []
    self.randomYs = np.random.choice(IMAGE_HEIGHT, NUM_RANDOM_POINTS, replace=False)
    self.randomXs = np.random.choice(IMAGE_WIDTH, NUM_RANDOM_POINTS, replace=False)

    for i in range(NUM_RANDOM_POINTS):
      point = self.randomXs[i], self.randomYs[i]
      self.pointsOfInterest.append(point)
    print("Points of interest:")
    print(self.pointsOfInterest)

  def didBump(self, observation):
    """
    didBump = False
    rgbdObs = observation[OBJ_KEY]
    depthValues = rgbdObs[DEPTH_CHANNEL, :, :]
    if (0 in depthValues):
      didBump = True
    #print("Depth values:" )
    #print(depthValues)

    print("Didbump: ")
    print(didBump)

    return didBump
    """
    #time.sleep(0.2)
    obs = observation[OBS_KEY]
    pix = obs[0,0]
    print("Pixel One : " + str(pix))
    pix = obs[IMAGE_WIDTH / 2, IMAGE_HEIGHT / 2]
    print("Pixel Mid : " + str(pix))
    time.sleep(0.01)

    didBump = False
    obs = observation[OBS_KEY]
    depths = obs[:,:, DEPTH_CHANNEL]
    #print("depths: ")
    #print(depths)
    minD = np.amin(depths)
    if minD == 0:
      print("Depth 0. Sleeping ...")
      time.sleep(5)
    maxD = np.amax(depths)
    avgD = np.average(depths)
    midPix = depths[IMAGE_HEIGHT / 2][IMAGE_WIDTH / 2]
    print("Min depth: " + str(minD))
    print("Max depth: " + str(maxD))
    print("average depth: " + str(avgD))
    print("mid point depth" + str(midPix))
    print("")
    #print("MinD: " + str(minD))
    #print("MaxD: " + str(maxD))
    didBump = minD < 160

    if didBump:
      print("BUMPED!!!!!")
      time.sleep(0.5)

    """
    depthArray = []
    #width, height
    for x in range(3):
      for y in range(2):
        depth = obs[DEPTH_CHANNEL, y,x]
        #print("x: " + str(x) + ", y: " + str(y) + ", depth: " + str(depth))
        depthArray.append(depth)
    if (0 in depthArray):
      didBump = True
    """
    #print("Did bump: " + str(didBump))

    return didBump

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
      phi.append(pixelRep)

      didBump = self.didBump(observation)


    return phi


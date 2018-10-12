#!/usr/bin/env python

"""Uses tilecoding to create state.

"""
import numpy as np
from tiles import *


# image tiles
NUM_RANDOM_POINTS = 100
CHANNELS = 4
NUM_IMAGE_TILINGS = 8
NUM_IMAGE_INTERVALS = 4
SCALE_RGB = NUM_IMAGE_INTERVALS / 256.0

IMAGE_START_INDEX = 0

# constants relating to image size recieved
IMAGE_HEIGHT = 480  # rows
IMAGE_WIDTH = 640  # columns

NUMBER_OF_CHANNELS = 3 #red, blue, green
PIXEL_FEATURE_LENGTH = np.power(NUMBER_OF_CHANNELS, NUM_IMAGE_INTERVALS) * NUM_IMAGE_TILINGS
TOTAL_FEATURE_LENGTH = PIXEL_FEATURE_LENGTH * NUM_RANDOM_POINTS

# Channels
RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2
DEPTH_CHANNEL = 3

class StateRepresentation(object):
  def __init__(self):
    self.pointsOfInterest = []
    self.randomYs = np.random.choice(IMAGE_HEIGHT, NUM_RANDOM_POINTS, replace=False)
    print("Random Ys")
    print(self.randomYs)
    self.randomXs = np.random.choice(IMAGE_WIDTH, NUM_RANDOM_POINTS, replace=False)
    print("RandomXs")
    print(self.randomXs)
    for i in range(NUM_RANDOM_POINTS):
      point = self.randomXs[i], self.randomYs[i]
      self.pointsOfInterest.append(point)
    print("Points of interest:")
    print(self.pointsOfInterest)



  def getPhi(self, observation):
    rgbdObs = observation['RGBD']
    #tilecode each pixel indivudually and then assemble

    phi = []

    for point in self.pointsOfInterest:
      #Get the pixel value at that point
      x = point[0]
      y = point[1]
      red = rgbdObs[RED_CHANNEL, y, x] / 256.0
      green = rgbdObs[GREEN_CHANNEL, y, x] / 256.0
      blue = rgbdObs[BLUE_CHANNEL, y, x] / 256.0

      pixelRep = np.zeros(PIXEL_FEATURE_LENGTH)
      #Tile code these 3 values together
      indexes = tiles(NUM_IMAGE_TILINGS, PIXEL_FEATURE_LENGTH, [red, green, blue])
      for index in indexes:
        pixelRep[index] = 1.0

      #Assemble with other pixels
      phi.append(pixelRep)

    return phi


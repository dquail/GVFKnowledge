# Representing Knowledge with layered predictions 
*An implementation using Deepmind lab*


## Abstract
This project demonstrates the ability for an AI agent to learn a prediction (the likelihood it will collide with a wall), and then change its behavior accordingly. The project uses the Deepmind Lab environment to form these predictions.

## Environment
The project uses the Deepmind Lab 3D virtual environment. This repository is a direct clone of https://github.com/deepmind/lab

Instructions below for getting the environment up and running (below) are borrowed from the Deepmind lab repository. Further instructions on usage can be found on that github repository.
 
## Getting started on Linux

* Get [Bazel from bazel.io](https://docs.bazel.build/versions/master/install.html).

* Clone DeepMind Lab, e.g. by running

```shell
$ git clone https://github.com/deepmind/lab
$ cd lab
```

We created a very simple maze by customizing [`game_scripts/levels/demos/map_generation/basic_level.lua`](game_scripts/levels/demos/map_generation/basic_level.lua)

This maze consists of a single room, with 4 walls, all the same color. 

Given this environment, we look to train the agent to predict when the agent will collide with the wall. This prediction is made via a General value function. The function predicts the value of the bump sensor, should it choose the 'forward' action. 
If a collision is predicted, the agent will choose to turn left. Otherwise the agent moves forward. 

This pavlovian control can be observed by running the following: 

```shell
lab$ bazel run :learning_agent --define graphics=sdl -- 
    --level_script=demos/map_generation/basic_level --length=10000 --width=640 --height=480
```
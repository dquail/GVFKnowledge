To create a different level:
- Created game_scripts/levels/demos/map_generation/basic_level.lua
--- This lua script contains the textual geometry of the walls.
--- It also sets the texture set to textures_sets.KNOWLEDGE (for walls, sky, floor etc). 

- Within game_scripts/themes, added another theme called KNOWLEDGE
--- This file references image files located in assets/
map/lab_games/ to specify the textures for walls etc.
--- This KNOWLEDGE theme also specifies what the floor looks like and if there is decals placed on walls.

To start the agent with this environment:
 $ bazel run :game -- --level_script=demos/map_generation/basic_level --level_setting=logToStdErr=true

bazel run :python_random_agent --define graphics=sdl -- --length=10000 --width=640 --height=480

bazel run :learning_agent --define graphics=sdl -- --level_script=demos/map_generation/basic_level --length=10000 --width=640 --height=480
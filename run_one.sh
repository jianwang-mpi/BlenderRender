#!/usr/bin/env bash
BLENDER_PATH=/home/wangjian02/Application/blender-2.78a-linux-glibc211-x86_64
$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 0 --model_path models
$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 120 --model_path models
$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 240 --model_path models
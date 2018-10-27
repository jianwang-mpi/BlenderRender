#!/usr/bin/env bash
BLENDER_PATH=/home/wangjian02/Application/blender-2.78a-linux-glibc211-x86_64

$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 0
$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 120
$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 240
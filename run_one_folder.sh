#!/usr/bin/env bash
BLENDER_PATH=/home/wangjian02/Application/blender-2.78a-linux-glibc211-x86_64
for model_dir in ${1}
do
echo $model_dir
for img_dir in `ls ${model_dir}/obj`
do
img_dir="${model_dir}/obj/"${img_dir}
$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 0 --model_path ${img_dir}
$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 120 --model_path ${img_dir}
$BLENDER_PATH/blender -b -t 1 -P render.py -- --angle 240 --model_path ${img_dir}
done
done

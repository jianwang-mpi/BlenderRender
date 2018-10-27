import bpy
import os
from math import radians
import argparse
import sys
def render(rotation_angle=0):
    context = bpy.context

    models_path = "/home/wangjian02/Projects/BlenderRender/models/"

    # create a scene
    scene = bpy.data.scenes.new("Scene")

    scene.render.resolution_x = 640
    scene.render.resolution_y = 960

    # bpy.data.scenes['Scene'].render.engine = 'CYCLES'

    world = bpy.data.worlds.get("World")
    scene.world = world
    world.use_nodes = True

    # changing these values does affect the render.
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value[:3] = (0.5, .1, 0.6)
    bg.inputs[1].default_value = 1.0

    scene.world.horizon_color = (1, 1, 1)

    camera_data = bpy.data.cameras.new("Camera")

    camera = bpy.data.objects.new("Camera", camera_data)
    camera.location = (0, 0.16, 2.5)
    camera.rotation_euler = ([radians(a) for a in (0.0, 0.0, 0.0)])
    # camera.rotation_euler = [0,  0,  0]
    scene.objects.link(camera)
    scene.camera = camera
    # Create new lamp datablock
    lamp_data = bpy.data.lamps.new(name="Lamp1", type='SUN')

    # Create new object with our lamp datablock
    lamp_object = bpy.data.objects.new(name="Lamp1", object_data=lamp_data)

    # Link lamp object to the scene so it'll appear in this scene
    scene.objects.link(lamp_object)
    bpy.data.lamps['Lamp1'].energy = 0.8
    # Place lamp to a specified location

    lamp_object.rotation_euler = (radians(240), radians(120), radians(0))

    # And finally select it make active
    lamp_object.select = True
    scene.objects.active = lamp_object

    # do the same for lights etc
    scene.update()

    # Create new lamp datablock
    lamp_data = bpy.data.lamps.new(name="Lamp2", type='SUN')

    # Create new object with our lamp datablock
    lamp_object = bpy.data.objects.new(name="Lamp2", object_data=lamp_data)

    # Link lamp object to the scene so it'll appear in this scene
    scene.objects.link(lamp_object)
    bpy.data.lamps['Lamp2'].energy = 0.8
    # Place lamp to a specified location

    lamp_object.rotation_euler = (radians(150), radians(30), radians(0))

    # And finally select it make active
    lamp_object.select = True
    scene.objects.active = lamp_object

    # do the same for lights etc
    scene.update()

    # Create new lamp datablock
    lamp_data = bpy.data.lamps.new(name="Lamp3", type='SUN')

    # Create new object with our lamp datablock
    lamp_object = bpy.data.objects.new(name="Lamp3", object_data=lamp_data)

    # Link lamp object to the scene so it'll appear in this scene
    scene.objects.link(lamp_object)

    # Place lamp to a specified location

    lamp_object.rotation_euler = (radians(0), radians(-60), radians(180))
    bpy.data.lamps['Lamp3'].energy = 0.8

    # And finally select it make active
    lamp_object.select = True
    scene.objects.active = lamp_object

    # do the same for lights etc
    scene.update()



    path = os.path.join(models_path, 'out.obj')
    # make a new scene with cam and lights linked
    context.screen.scene = scene
    bpy.ops.scene.new(type='LINK_OBJECTS')
    context.scene.name = 'out.obj'
    cams = [c for c in context.scene.objects if c.type == 'CAMERA']
    bpy.ops.import_scene.obj(filepath=path, axis_forward='X', axis_up='-Z', filter_glob="*.obj;*.mtl")
    ob = context.scene.objects[0]
    ob.rotation_euler = (radians(180), radians(rotation_angle), 0)

    print('----------------------')
    print(bpy.data.materials.keys())
    bpy.data.materials['lambert1'].use_shadeless = True

    for c in cams:
        context.scene.camera = c
        print("Render ", 'out.obj', context.scene.name, c.name)
        context.scene.render.filepath = "output_rotate_{}".format(rotation_angle)
        bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate synth dataset images.')
    parser.add_argument('--angle', type=int,
                        help='rotation angle')
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    render(rotation_angle=args.angle)

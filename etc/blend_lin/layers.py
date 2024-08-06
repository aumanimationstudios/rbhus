#!/usr/bin/env python3
import bpy
for x in bpy.context.scene.render.layers:
  bpy.context.scene.render.layers[x.name].use = False
bpy.context.scene.render.layers['shadows'].use = True


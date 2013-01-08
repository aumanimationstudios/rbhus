#!/usr/bin/python3
import bpy
import os
outputDir = "renameOutputDir"
scenes = bpy.data.scenes.keys()

for x in scenes:
  nodes = bpy.data.scenes[x].node_tree.nodes.keys()
  for n in nodes:
    if(n.find("File Output") >= 0):
      bpy.data.scenes[x].node_tree.nodes[n].base_path = outputDir.rstrip("/") + "/" + bpy.data.scenes[x].node_tree.nodes[n].inputs[''].links[0].from_socket.name

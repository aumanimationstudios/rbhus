#!/usr/bin/env python3
import bpy
import os
outputDir = "renameOutputDir"
scenes = bpy.data.scenes.keys()
renderLayer = "renameRenderLayer"
for x in scenes:
  nodes = bpy.data.scenes[x].node_tree.nodes.keys()
  for n in nodes:
    if(n.find("File Output") >= 0):
      try:
        if(renderLayer != "renameRenderLayer"):
          if(bpy.data.scenes[x].node_tree.nodes[n].inputs[0].links[0].from_node.layer == renderLayer):
            bpy.data.scenes[x].node_tree.nodes[n].base_path = outputDir.rstrip("/") + "/" + bpy.data.scenes[x].node_tree.nodes[n].inputs[0].links[0].from_socket.name
            print("output path : "+ str(bpy.data.scenes[x].node_tree.nodes[n].base_path))
        else:
          bpy.data.scenes[x].node_tree.nodes[n].base_path = outputDir.rstrip("/") + "/" + bpy.data.scenes[x].node_tree.nodes[n].inputs[0].links[0].from_socket.name
      except:
        print("fuck!!! .. output node not connected : "+ str(n))

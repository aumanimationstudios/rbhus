#!/usr/bin/python
import os
from flask import Flask,request,render_template

video_dir = '/blueprod/STOR2/stor2/stor1/crap/Movies/Animated_Movies'

app = Flask(__name__)

@app.route('/blueprod/STOR2/stor2/stor1/crap/Movies/Animated_Movies')

def hello_world():
  return 'Hello World!'

if(__name__ == "__main__"):
  app.run()
  
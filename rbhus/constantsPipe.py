###
# Copyright (C) 2012  Shrinidhi Rao shrinidhi@clickbeetle.in
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###
import os
import tempfile
import sys
import debug

tempDir = tempfile.gettempdir()
file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
debug.info(base_dir)

#proj table

projActive = 1
projDeactive = 0

projInitPort = 9666
projInitServer = "blues2"


createStatusInit = 0
createStatusPending = 1
createStatusRunning = 2
createStatusDone = 3
createStatusFailed = 4

createStatus = {
  0 : "Initiating",
  1 : "Pending",
  2 : "creating",
  3 : "done",
  4 : "failed"
}

assetStatusDelete = 0
assetStatusActive = 1
assetStatusHidden = 2
assetProgressInProgress = 0
assetProgressDone = 1
assetProgressNotStarted = 2


reviewStatusNotDone = 0
reviewStatusInProgress = 1
reviewStatusDone = 2

run_api_cmd_review = "review"


typesActive = 1
typesDeactive = 2
typesHidden = 3
typesAll = 4

mediaMime = {
             "image":[".png",".jpg",".jpeg",".exr",".svg"],
             "video":[".avi",".mp4",".mpg",".mov"],
             "audio":[".mp3",".wav",".flac"],
             "blender":[".blend",".blend1",".blend2"]
            }

mimeLogo = {
  "image" : os.path.join(base_dir,"etc","icons","mime_type_image.png"),
  "video" : os.path.join(base_dir,"etc","icons","mime_type_video.png"),
  "blender" : os.path.join(base_dir,"etc","icons","mime_type_blender.png"),
  "audio" : os.path.join(base_dir,"etc","icons","mime_type_audio.png")
}

mimeConvertCmd = {
  "image": "/usr/bin/convert '{0}' -resize 256x256 '{1}'",
  "video": "/usr/bin/convert '{0}'[23] -resize 256x256 '{1}'",
  "blender": os.path.join(base_dir,"tools","rbhus","blender-thumbnailer.py") +" '{0}' '{1}'"
}


ignoreTemplateTypes = ["share","bin","output","template"]
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

tempDir = tempfile.gettempdir()
file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
sys.path.append(base_dir)
import rbhus.debug as debug
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
assetProgressInProgress = 1
assetProgressDone = 2
assetProgressNotStarted = 0


reviewStatusNotDone = 0
reviewStatusInProgress = 1
reviewStatusDone = 2

run_api_cmd_review = "review"


typesActive = 1
typesDeactive = 2
typesHidden = 3
typesAll = 4

mimeTypes = {
             "image":[".png",".jpg",".jpeg",".exr",".svg",".tiff",".tga",".hdr"],
             "video":[".avi",".mp4",".mpg",".mov",".gif",".webp"],
             "audio":[".mp3",".wav",".flac"],
             "blender":[".blend",".blend1",".blend2"],
             "office":[".ods",".doc",".xls",".xlsx",".txt",".docx"],
             "krita":[".kra"],
             "psd":[".psd"],
             "pdf":[".pdf"],
             "reel":[".reel"],
             "pureref":[".pur"],
             # "edl":[".reel"]
            }

mimeLogos = {
  "image" : os.path.join(base_dir,"etc","icons","mime_type_image.png"),
  "video" : os.path.join(base_dir,"etc","icons","mime_type_video.png"),
  "blender" : os.path.join(base_dir,"etc","icons","mime_type_blender.png"),
  "audio" : os.path.join(base_dir,"etc","icons","mime_type_audio.png"),
  "office":os.path.join(base_dir,"etc","icons","mime_type_office.png"),
  "krita" : os.path.join(base_dir,"etc","icons","mime_type_krita.png"),
  "psd": os.path.join(base_dir,"etc","icons","mime_type_psd.png"),
  "pdf": os.path.join(base_dir,"etc","icons","mime_type_pdf.png"),
  "reel": os.path.join(base_dir,"etc","icons","mime_type_reel.png"),
  "pureref": os.path.join(base_dir,"etc","icons","mime_type_pureref.png"),
}

mimeConvertCmds = {
  "image": "/usr/bin/magick \"{0}\" -sample 96x96 \"{1}\"",
  "pdf": "/usr/bin/magick \"{0}\"[0] -sample 96x96 -alpha remove \"{1}\"",
  # "video": "/usr/bin/convert \"{0}[1]\" -sample 96x96 \"{1}\"",
  "video": "/usr/bin/ffmpeg -loglevel panic -i \"{0}\" -vframes 1 -an -vf scale=96:-1 -ss 0.1 -y \"{1}\"",
  "office" : "cp "+ os.path.join(base_dir,"etc","icons","libreOffice_logo.png") +" \"{1}\"",
  "blender": os.path.join(base_dir,"tools","rbhus","blender-thumbnailer.py") +" \"{0}\" \"{1}\"",
  "krita": os.path.join(base_dir,"tools","rbhus","krita-thumbnailer.py") +" \"{0}\"  \"{1}\"",
  "pureref": "cp "+ os.path.join(base_dir,"etc","icons","pureref.png") +" \"{1}\""
}

mimeTypesOpenCmds = {
  "image": {"linux":["gwenview","djv_view - image","djv_view - sequence","djv_view_v2","krita","inkscape","mrViewer"]},
  "video": {"linux":["mpv - loop","mpv", "djv_view - video","mrViewer"]},
  "blender": {"linux":["project_assigned_application"]}, # Just enter "project_assigned_application" to open certain kinds of files with project assigned apps.
  "pdf": {"linux":["system_assigned_application"]}, # Just enter "system_assigned_application" to open certain kinds of files with project assigned apps.
  "krita": {"linux":["krita"]},
  "office": {"linux":["libreoffice","gnumeric","abiword"]},
  "audio": {"linux":["mpv-audio","mpv-audio - loop"]},
  "psd": {"linux":["krita"]},
  "reel": {"linux":["mrViewer"]},
  "pureref": {"linux":["pureref"]},
  # "edl": {"linux":["mrViewer"]},
}



mimeCmdsLinux = {
  "gwenview"                     : "gwenview {0}",
  "djv_view - image"             : "djv_view -seq_auto False -file_cache False {0}",
  "djv_view - sequence"          : "djv_view -seq_auto True {0}",
  "djv_view_v2"                   : "djv_view_v2 {0}",
  "mrViewer"                     : "mrViewer.sh --playback --run -e {0}",
  "mpv"                          : "mpv --window-scale=0.5 --really-quiet {0}",
  "mpv-audio"                    : "mpv --player-operation-mode=pseudo-gui --really-quiet {0}",
  "mpv - loop"                   : "mpv --window-scale=0.5 --really-quiet --loop {0}",
  "mpv-audio - loop"             : "mpv --player-operation-mode=pseudo-gui --really-quiet --loop {0}",
  "djv_view - video"             : "djv_view -file_cache False {0}",
  "krita"                        : "krita {0}",
  "libreoffice"                  : "libreoffice --nologo {0}",
  "gnumeric"                     : "gnumeric {0}",
  "abiword"                      : "abiword {0}",
  "inkscape"                     : "inkscape {0}",
  "pureref"                      : "pureref {0}"
}

ignoreTemplateTypes = ["share","bin","output","template"]

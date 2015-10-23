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

#proj table

projActive = 1
projDeactive = 0

projInitPort = 9666
projInitServer = "192.168.1.198"


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


reviewStatusNotDone = 0
reviewStatusInProgress = 1
reviewStatusDone = 2
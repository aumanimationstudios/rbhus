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


#task table
taskWaiting = 0
taskPending = 1
taskActive = 2
taskStopped = 3
taskAutoStopped = 5
taskDone = 4

taskStatus = {
  0 : "waiting",
  1 : "pending",
  2 : "active",
  3 : "stopped",
  4 : "done",
  5 : "autoStopped"
}


#frames table
framesUnassigned = 0
framesAssigned = 1
framesPending = 2
framesRunning = 3
framesDone = 4
framesFailed = 5
framesHold = 6
framesAutoHold = 7
framesKilled = 9


framesStatus = {
  0 : "unassigned",
  1 : "assigned",
  2 : "pending",
  3 : "running",
  4 : "done",
  5 : "failed",
  6 : "hold",
  7 : "autoHold",
  9 : "killed"
}

#hostInfo table
hostInfoDisable = 0
hostInfoEnable = 1

hostInfoStatus = {
  0 : "enabled",
  1 : "disabled"
}

#hostAlive table
hostAliveDead = 0
hostAliveAlive = 1

#hostResource
hostResourceActive = 1
hostResourceStopped = 2
hostResourceForcedOff = 3
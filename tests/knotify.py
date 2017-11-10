#! /usr/bin/python
import sys, dbus

knotify = dbus.SessionBus().get_object("org.kde.Notifications", "/Notify")
try:
  title, text = "test", "wtf1"
except:
  print 'Usage: knotify.py title text'; sys.exit(1)
knotify.event("warning", 1, [], title, text, [], ['Accept'], 0, 0, dbus_interface="org.kde.KNotify")

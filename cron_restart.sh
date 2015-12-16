#!/bin/sh
sleep 20
/etc/local.d/01-rbhus.stop
sleep 5
/etc/local.d/01-rbhus.start

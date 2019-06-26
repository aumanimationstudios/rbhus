#!/bin/bash
sleep 60

/etc/local.d/01-rbhus.stop
sleep 10
/etc/local.d/01-rbhus.start


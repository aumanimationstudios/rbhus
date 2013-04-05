#!/sbin/runscript
# Copyright 1999-2011 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/app-crypt/heimdal/files/heimdal-kcm.initd-r1,v 1.1 2011/02/16 22:14:12 eras Exp $


start() {
	ebegin "Starting rbhusDrone..."
	sleep 30
	/opt/rbhus/rbhusDrone.sh
	eend $?
}

stop() {
	ebegin "Stopping rbhusDrone..."
	pkill -9 rD
	eend $?
}

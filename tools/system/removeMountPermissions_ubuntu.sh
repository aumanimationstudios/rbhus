#!/bin/bash
rm -fv /usr/share/polkit-1/actions/org.freedesktop.udisks2.policy
mv /usr/share/polkit-1/actions/org.freedesktop.udisks2.policy.old /usr/share/polkit-1/actions/org.freedesktop.udisks2.policy

#!/bin/bash
tree -aif | grep -i pyc$ | xargs rm -fv
tree -aif | grep -i ~$ | xargs rm -fv
tree -aif | grep -i swp$ | xargs rm -fv

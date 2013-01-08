#!/bin/bash
tree -aif | grep -i pyc$ | xargs rm -frv
tree -aif | grep -i ~$ | xargs rm -frv
tree -aif | grep -i swp$ | xargs rm -frv

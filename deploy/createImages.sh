#!/bin/bash

cwd=`pwd`

echo 'Creating image ui-meetmyinterests'
cd $cwd/ui-meetmyinterests
make dockerstage

echo 'Creating image service-interests'
cd $cwd/service-interests
make dockerstage

echo 'Creating image service-auth'
cd $cwd/service-auth
make dockerstage

echo 'Creating image service-blog'
cd $cwd/service-blog
make dockerstage
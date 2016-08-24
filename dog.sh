#!/bin/sh

progress="python server.py"

ps -fe|grep "$progress" |grep -v grep
if [ $? -ne 0 ]
then
echo "start process....."
$progress &
else
echo "runing....."
fi

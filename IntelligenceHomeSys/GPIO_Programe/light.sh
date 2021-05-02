#!/bin/bash
if [ $# > 1 ]
then
/usr/local/bin/gpio mode 4 out
    if [[ "$1" = "on" ]]
    then
/usr/local/bin/gpio write 4 on
    fi
 
    if [[ "$1" = "off" ]]
    then
/usr/local/bin/gpio write 4 off
    fi
fi
#!/bin/sh

#Download the keep_wifi.sh and place it in some convenient folder - it could be your python folder, or just your home folder
#on the command line, change directory to the folder with keep_wifi.sh
#run this:

#chmod +x keep_wifi.sh
#When you want to run it, open up a terminal, change directory to the folder with keep_wifi.sh and do:

#./keep_wifi.sh
#you can minimize the terminal window if you want to get it out of the way.



while :
do
    ping -c4 10.2.2.1 > /dev/null

    if [ $? != 0 ]
    then
    echo "No network connection, restarting wlan0"
    sudo ifconfig wlan0 up
    else
    echo -n "."
    fi

    sleep 10
done

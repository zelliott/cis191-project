#!/bin/bash

# Removes all created pipes
function rmPipes() {
	sendPipe=$1
	receivePipe=$2

	if [ -p "$sendPipe" ]
	then
		rm $sendPipe
	fi

	if [ -p "$receivePipe" ]
	then
		rm $receivePipe
	fi
}

# Create pipes

sendPipe="/tmp/sgcli-send"
receivePipe="/tmp/sgcli-receive"

rmPipes $sendPipe $receivePipe

mkfifo $sendPipe
cat > $sendPipe &
sendPid=$!

mkfifo $receivePipe
cat > $receivePipe &
receivePid=$!

# Spawn background Python process

python sgrunner.py &

# Check to see if the user specified an action

if [[ $# -eq 0 ]]
then
	echo "No action specified.  Try one of the following:"
	echo "--order"
	echo "--scheduledOrder"
	echo "--removeScheduledOrder"
	echo "--addAccount"
	echo "--removeAccount"
	echo "--changeAccount"
else
	case ${1} in
		"--order")
			./actions/performOrder.sh
			;;
		"--scheduledOrder")
			./actions/performOrder.sh "-s"
			;;
		"--removeScheduledOrder")
			./actions/performRemoveScheduledOrder.sh
			;;
		"--addAccount")
			./actions/performAddAccount.sh
			;;
		"--removeAccount")
			./actions/performRemoveAccount.sh
			;;
		"--changeAccount")
			./actions/performChangeAccount.sh
			;;
	esac
fi

# Remove all pipes, destroy all created processes

rmPipes $sendPipe $receivePipe

disown $sendPid
kill -9 $sendPid &> /dev/null
disown $receivePid
kill -9 $receivePid &> /dev/null
pkill -f sgrunner.py > /dev/null
#!/bin/bash

# Creates a scheduled order
function performScheduledOrder() {
	zipCode=$1
	locationNo=$2
	itemNo=$3

	min=$((0))
	hr=$((1))

	echo "Please specify when this order should be scheduled as follows:"
	echo "Day of wk (0-6 or *) Month (1 - 12 or *) Day of month (1 - 31 or *)"
	echo "(e.g. > 0 9 20)"
	read -p "> " dow mo dom

	# Validate schedule
	idow=$(($dow + 0))
	imo=$(($mo + 0))
	idom=$(($dom + 0))

	if [ \( $idow -l 0 -o $idow -g 6 \) -a \( $dow != "*" \) ]
	then
		echo "Invalid day of week."
		exit
	fi

	if [ \( $imo -l 1 -o $imo -g 12 \) -a \( $mo != "*" \) ]
	then
		echo "Invalid month."
		exit
	fi

	if [ \( $idom -l 1 -o $idom -g 31 \) -a \( $dom != "*" \) ]
	then
		echo "Invalid day of month."
		exit
	fi

	pickupTimes="11:00am 12:00pm 1:00pm 2:00pm 3:00pm 4:00pm 5:00pm 6:00pm 7:00pm 8:00pm 9:00pm"

		# Choose pickup time
	echo "Choose a pickup time:"
	i=$((0))
	for time in $pickupTimes
	do
		echo "$i) $time"
		i=$(($i+1))
	done
	read -p "> " timeNo

	# Validate time choice
	timeNo=$(($timeNo + 0))
	if [ $timeNo -le 0 -a $timeNo -ge $((i)) ]
	then
		echo "Invalid time choice."
		exit
	fi

		# Prompt for password to confirm order
	echo "Enter your sweetgreen password to confirm your order:"
	read -p "> " password

	fullpath="$(realpath ./api/scheduleOrder.py)"

	(crontab -l && echo "$min $hr $dom $mo $dow python $fullpath $zipCode $locationNo $itemNo $timeNo $password") | crontab -

	echo "$min $hr $dom $mo $dow python $fullpath $zipCode $locationNo $itemNo $timeNo $password" >> ./.sgcli/scheduledOrders
	echo "Order scheduled"
}

performScheduledOrder $1 $2 $3
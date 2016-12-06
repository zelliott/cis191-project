#!/bin/bash

# Creates a normal order
function performOrder() {
	flag=$1

	echo "Enter your zip code:"
	read -p "> " zipCode

	# Get locations
	locations="$(python ./api/getLocationsFromZipCode.py $zipCode)"

	# Error handling if no locations
	if [ -z "$locations" ]
	then
		echo "No locations for this zip code"
		exit
	fi

	# Choose location
	echo "Choose a location from the below list:"
	i=$((0))
	for location in $locations
	do
		echo "$i) $location"
		i=$(($i+1))
	done
	read -p "> " locationNo

	# Validate location choice
	locationNo=$(($locationNo + 0))
	if [ $locationNo -le 0 -a $locationNo -ge $((i)) ]
	then
		echo "Invalid zip code choice."
		exit
	fi

	# Get menu
	menu="$(python ./api/getMenuFromLocation.py $locationNo)"

	# Error handling if no menu
	if [ -z "$menu" ]
	then
		echo "No menu for this location"
		exit
	fi

	# Choose menu item
	echo "Choose a salad from the below list:"
	i=$((0))
	for item in $menu
	do
		echo "$i) $item"
		i=$(($i+1))
	done
	read -p "> " itemNo

	# Validate item choice
	itemNo=$(($itemNo + 0))
	if [ $itemNo -le 0 -a $itemNo -ge $((i)) ]
	then
		echo "Invalid item choice."
		exit
	fi

	# If this is a scheduled order, we have to handle things
	# slightly differently via cronjobs
	if [ "$flag" == "-s" ]
	then
		./actions/performScheduledOrder.sh $zipCode $locationNo $itemNo
		exit
	fi

	# Get pickupTimes
	pickupTimes="$(python ./api/getPickupTimesFromItem.py $itemNo)"

	# Error handling if no pickup times
	if [ -z "$pickupTimes" ]
	then
		echo "No pickup times for this item"
		exit
	fi

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

	# Validate password & get user data
	order="$(python ./api/confirmOrder.py $timeNo $password)"

	order=$(($order + 0))
	if [ $order -eq 0 ]
	then
		echo "Order failed"
		exit
	else
		echo "Order submitted"
	fi
}

performOrder $1
#!/bin/bash

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
		performScheduledOrder $zipCode $locationNo $itemNo
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

function performRemoveScheduledOrder() {
	scheduledOrder="$(cat ./.sgcli/scheduledOrders)"
	crontab -l | grep -v "$scheduledOrder" | crontab -
	rm ./.sgcli/scheduledOrders

	echo "Order removed"
}

function performAddAccount() {
	echo "Enter your account information one at a time (8 total lines):"
	echo "Email (1/8)"
	read -p "> " email
	echo "Password (2/8)"
	read -p "> " password
	echo "Card number (3/8)"
	read -p "> " cardNo
	echo "Expiration month (4/8)"
	read -p "> " expMo
	echo "Expiration year (5/8)"
	read -p "> " expYr
	echo "CVV (6/8)"
	read -p "> " cvv
	echo "Postal code (7/8)"
	read -p "> " postalCode
	echo "Contact number (8/8)"
	read -p "> " contactNum

	# Add account information
	accountAdded="$(python ./api/addAccount.py $email $password $cardNo $expMo $expYr $cvv $postalCode $contactNum)"

	accountAdded=$(($accountAdded + 0))
	if [ $accountAdded -eq 0 ]
	then
		echo "Account was not added"
		exit
	else
		echo "Account was successfully added"
	fi
}

function performRemoveAccount() {
	rm -rf ./.sgcli
}

function performChangeAccount() {
	echo "Enter the number of the account field to change:"
	echo "0) Email"
	echo "1) Password"
	echo "2) Card number"
	echo "3) Expiration month"
	echo "4) Expiration year"
	echo "5) CVV"
	echo "6) Postal code"
	echo "7) Contact number"
	read -p "> " changeAccountOption

	case $changeAccountOption in
		0)
			flag="--email"
			field="email"
			;;
		1)
			flag="--password"
			field="password"
			;;
		2)
			flag="--cardNo"
			field="card number"
			;;
		3)
			flag="--expMo"
			field="expiration month"
			;;
		4)
			flag="--expYr"
			field="expiration year"
			;;
		5)
			flag="--cvv"
			field="cvv"
			;;
		6)
			flag="--postalCode"
			field="postal code"
			;;
		7)
			flag="--contactNum"
			field="contact number"
			;;
		*)
			echo "Invalid account choice."
			exit
	esac

	echo "Enter your password to verify change:"
	read -p "> " password

	echo "Enter your new $field:"
	read -p "> " value

	accountChanged="$(python ./api/changeAccount.py $flag $value $password)"

	accountChanged=$(($accountChanged + 0))
	if [ $accountChanged -eq 0 ]
	then
		echo "Account was not changed"
		exit
	else
		echo "Account was successfully changed"
	fi
}

mkfifo /tmp/sgcli-send
cat > /tmp/sgcli-send &
sendPid=$!

mkfifo /tmp/sgcli-receive
cat > /tmp/sgcli-receive &
receivePid=$!

python sgrunner.py &

if [[ $# -eq 0 ]]
then
	echo "Specify a command"
else
	case ${1} in
		"--order")
			performOrder
			;;
		"--scheduledOrder")
			performOrder "-s"
			;;
		"--removeScheduledOrder")
			performRemoveScheduledOrder
			;;
		"--addAccount")
			performAddAccount
			;;
		"--removeAccount")
			performRemoveAccount
			;;
		"--changeAccount")
			performChangeAccount
			;;
	esac
fi

kill $sendPid
kill $receivePid
pkill -f sgrunner.py
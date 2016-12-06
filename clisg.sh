#!/bin/bash

# TODO: ZACK:
# The below code is being kept for reference
# and should not be uncommented.

# email=${userData[0]}
# password=${userData[1]}
# cardNo=${userData[2]}
# expMo=${userData[3]}
# expYr=${userData[4]}
# cvv=${userData[5]}
# postalCode=${userData[6]}
# contactNum=${userData[7]}

function performOrder {
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

# function performAddPayment() {
# 	echo "Add payment"
# }

mkfifo /tmp/sgcli-send
cat > /tmp/sgcli-send &
sendPid=$!

mkfifo /tmp/sgcli-receive
cat > /tmp/sgcli-receive &
receivePid=$!

python runner.py &

if [[ $# -eq 0 ]]
then
	echo "Specify a command"
else
	case ${1} in
		"--order")
			performOrder
			;;
		"--addAccount")
			performAddAccount
			;;
		# "--addPayment")
		# 	performAddPayment
		# 	;;
	esac
fi

kill $sendPid
kill $receivePid

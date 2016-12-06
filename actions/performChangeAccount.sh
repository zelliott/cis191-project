#!/bin/bash

# Changes an account
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

performChangeAccount
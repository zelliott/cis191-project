#!/bin/bash

# Adds an account
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

	accountAdded="$(python ./api/addAccount.py $email $password $cardNo $expMo $expYr $cvv $postalCode $contactNum)"

	accountAdded=$(($accountAdded + 0))
	if [ $accountAdded -eq 0 ]
	then
		echo "Account was not added"
	else
		echo "Account was successfully added"
	fi
}

performAddAccount
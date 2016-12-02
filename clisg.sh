#!/bin/bash

##This bash script takes in inputs for a command-line Sweetgreen ordering program.
##flags: --createAccount --paymentDetails --login
## --createAccount: locally stores firstname, lastname, email, password, and phone number to populate creating a new account on sweetgreen.com
## --paymentDetails: locally stores card number, expiration month, expiration year, CCV code, billing zip 
## --login: locally stores an email and password, which will be used to log into an account on sweetgreen.com

firstname=null
lastname=null
email=null
password=null
phonenumber=null
cardnumber=null
exp_month=null
exp_year=null
ccv_code=null
billing_zip=null
zipcode=null
pickup_time=null
bowl_type=null

case $# in
	1)
	case $1 in
		-createAccount)
			echo "You need to create an account before you can order from SG."
			echo "Please provide firstname, lastname, email, password, and phone number you want to use to create your account."
		i	read firstname_in lastname_in email_in password_in phonenumber_in
			firstname=$firstname_in
			lastname=$lastname_in
			email=$email_in
			password=$password_in
			phonenumber=$phonenumber_in
		;;
		-paymentDetails)
			echo "Please provide payment details: card number, expiration month, exp. year, CCV code, and billing zip."
			read cardnumber_in exp_month_in exp_year_in ccv_code_in billing_zip_in
			cardnumber=$cardnumber_in
			exp_month=$exp_month_in
			exp_year=$exp_year_in
			ccv_code=$ccv_code_in
			billing_zip=$billing_zip_in
		;;
		-login)
			echo "Please provide email, then password."
			read email_in password_in
			
			email=$email_in
			password=$password_in	
		;;
		esac
	;;
	0)
		echo "Please provide your ZIP code, desired pickup time (no spaces), and bowl_type."
		read zipcode_in pickup_time_in bowl_type_in
		
		##TODO-- regex to parse pickup time, bowl_type
		
		zipcode=$zipcode_in
		pickup_time=$pickup_time_in
		bowl_type=$bowl_type_in
	;;
	esac



##Raghav call python web req script from here using variables above as command-line args

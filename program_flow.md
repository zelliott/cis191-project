### Ordering

1. `./clish.sh --order`
2. Prompts user for zipcode
3. Based upon zipcode input, display locations for user to choose from
4. Based upon location selection, display salads for user to choose from
5. Initiate checkout process:
  * Prompt user for password to finalize & confirm order
  * If password is correct, grab all user info from data.json
  * Use the user info to place order.
  * Display some kind of success message
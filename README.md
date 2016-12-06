Group Members: Zack Elliott, Alessandro Portela, Raghav Joshi

## To Run:

*Note: Most of these commands will kick off a series of prompts for you to enter information.*

1. Add an account:

```
$ ./sgcli.sh --addAccount
```

2. Change any account information:

```
$ ./sgcli.sh --changeAccount
```

3. Remove your account information:

```
$ ./sgcli.sh --removeAccount
```

4. Place an order:

```
$ ./sgcli.sh --order
```

### Project Description / Goals:

Our team has built a command-line program for ordering from Sweetgreen.  This program includes the following major components:

* Restaurant Location: Logic that either accepts a particular preferred location to order from, or helps the user find the nearest Sweetgreen.
* Order Processing: Our program must process the order and interact with Sweetgreen’s online checkout portal.
* Secure Payment and Authentication: Our program will need to securely store all payment and authentication information on the user's computer.
* Scheduled Orders:  The ability to create a cron job to submit an order at a particular date/time.
* Command-Line Interface: An easy to understand CLI for specifying all aspects of ordering.  For example, users will be able to specify menu items (e.g. salad types, sides, drinks, etc...), specific customizations, as well as other details of their order (e.g. type of payment, location, special instructions).

*Note:*

Our project proposal changed to ordering from Sweetgreen from ordering to Chipotle because Chipotle's online ordering portal was offline for maintenance this last weekend.  Given that our group was not sure when the portal would be back up, we decided that it would be a smart idea to switch to a different restaurant.  We chose Sweetgreen because, although they do not have an "official" API, many of the requests being made on their website are prefixed with `/api/`, and thus it seemed like we would be able to identify which to use.

### Project Structure:

`sgcli.sh`

Our program runs through the shell script `sgcli.sh`, which kicks off all other helping programs/scripts.  First, this script sets up two *named pipes* called `/tmp/sgcli-send` and `/tmp/sgcli-receive`.  These pipes are used by our various Python scripts to communicate to one another.  Second, it kicks off `runner.py` in the background.  Third, it handles all user I/O in our program.  This involves (1) parsing command line arguments such as `--order` and `--addAccount`, (2) reading user input and sending it to the various Python scripts, and (3) validating user input and displaying success/error messages.  Finally, this script cleans up all processes and pipes it creates at the end of running.

`runner.py`

This Python script is called by `sgcli.sh`, and essentially just loops in a non-blocking read loop, reading input from the pipe `/tmp/sgcli-send`.  Whenever input comes in, it parses the input to determine what it should do, and what it should send back to the pipe `/tmp/sgcli-receive`.  For example, if the input `--getLocations 19104` is sent to `runner.py`, then the program parses `--getLocations` to determine that it should return a list of restaurant locations specific to that particular zip code.  Thus, this script can be thought of as the middleman between `sgcli.sh` (which handles all I/O with the user) and `scrape.py` (which actually performs all of the hard work of making requests to Sweetgreen's API).

`scrape.py`

As mentioned above, this script holds all logic regarding making requests to Sweetgreen's various endpoints, parsing response JSON, and sending that data back to `runner.py` to eventually be piped back to `sgcli.sh`.

`api/`

These Python programs are simply helper methods used by `sgcli.sh` and `runner.py` to send data back and forth through the pipes.  They're not super interesting.

`saver/secure_saver.py`

This Python program handles all aspects of saving and encrypting sensitive account data to the user's computer.  When it is called, it first creates a folder & file `.sgcli/data.json`.  This JSON file will hold all account information needed by our program to submit an order to Sweetgreen (i.e. Sweetgreen account information, credit card data, etc...).

The class works in the following manner.  First, the JSON data blob is stored in the file along with a required password.  The password is hashed using SHA512 with a random salt, and both are included in the JSON blob.  Then, whenever information needs to be retrieved from the `data.json` file, a password is required, and the SecureSaver class verifies that the hashed passwords match.  If so, it returns the data.  Whenever information needs to be stored in the file, again, a password is required, and the class ensures the hashes match.  If so, it updates the blob accordingly.

Additionally, all data other than the password and the salt are encrypted using a basic XOR encryption (not super secure, but more of a proof of concept).  This means that if a user opens the `data.json` file, then they will be unable to read any sensitive data (e.g. credit card numbers will be jumbled).

### Zack:

I worked primarily on the central shell script, securely saving user data on the computer, and helping Raghav parse Sweetgreen requests/responses and general API.
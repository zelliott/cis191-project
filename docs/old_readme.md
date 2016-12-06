Group Members: Zack Elliott, Alessandro Portela, Raghav Joshi

### Project Description:

Our team is building a command-line program for ordering Chipotle.  This program includes the following major components:

Restaurant Location: Logic that either accepts a particular preferred location to order from, or helps the user find the nearest Chipotle.
Order Processing: Our program must process the order and interact with Chipotle’s online checkout portal.
Secure Payment and Authentication: Our program will need to securely store all payment and authentication information.
Scheduled Orders:  The ability to create a cron job to submit an order at a particular date/time.
Command-Line Interface: An easy to understand CLI for specifying all aspects of ordering.  For example, users will be able to specify menu items (e.g. burrito, bowl, quesadilla), specific customizations (e.g. black or pinto beans), as well as other details of their order (e.g. type of payment, location, special instructions).

### Milestones:

We still need to research many aspects of this program, and so the following milestones are tentative as new information comes to light.

 * 11/7: Complete all project research and divide up tasks amongst group members.
 * 11/14: Finish the bulk of the order processing logic.
 * 11/21: Securely handle all payment and authentication information
 * 11/28: Finetune the command-line interface, enable more detailed arguments to call the script by.
 * 12/5: Complete identifying the nearest restaurant and scheduled orders.

### Project Design:

We will be using Python and shell scripts to build the main logic of our program.  A similar tool purporting to access Chipotle via some API is open sourced and written in JavaScript, and should be a helpful resource for examining what endpoints we can call to send orders to Chipotle.

We will have to devise some secure way to store credit card and Chipotle account information on the user’s computer (clearly not in plaintext).   This information could be encrypted with some kind of private master key that the user remembers.  Additionally, currently the plan is to release this command-line tool for unix-based operating systems only, but this may change.

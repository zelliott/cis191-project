### Project Structure

#### clisg.sh

The central runner that is kicked off when this command line program runs.
It kicks off the `app.py` program (which handles all communication with sweetgreen) and handles all I/O with the user.

#### app.py

Handles all communication with sweetgreen.  Input is sent to this program through 'named pipes' via the methods in `/api`.  This program outputs back to the `/api` functions.

#### /api

These functions are called by `clisg.sh`, send data to `app.py`, and print data back for `clisg.sh` to work with.



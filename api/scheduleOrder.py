import sys

zipCode = sys.argv[1]
locationNo = sys.argv[2]
itemNo = sys.argv[3]
timeNo = sys.argv[4]
password = sys.argv[5]

# TODO:
# This script will be executed by the user's crontab at some point in the future.
# Thus, all this script needs to do is execute the same series of API calls as in the normal
# ordering process.
# All required information to place an order is listed above.
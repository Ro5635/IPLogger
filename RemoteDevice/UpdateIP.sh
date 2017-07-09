# This checks the current IP Address and compares it with the IP address that was used in the
# last update, if it has changed it calls the API and updates the IP address and saves the 
# updated value to the file specified IPSaveLocation.
# This script should be executed at an interval (10 mins?) on the remote PC Whose IP is to be
# tracked.

# Location to save the last IP
IPSaveLocation=/tmp/IPTracker/LastIP

# Get the current External IP address
currentExtIP=$(dig +short myip.opendns.com @resolver1.opendns.com)

# Check to see if this IP is the same as the last submitted IP
lastSubmittedIP=$(cat $IPSaveLocation)

echo "The last IP: $lastSubmittedIP"

echo "Current IP: $currentExtIP"


# Has the IP changed since the last update?
if [ "$lastSubmittedIP" == "$currentExtIP" ]; then
	# The IP is the same!

	# Nothing to do, exit.
	echo "IP Unchanged"
else
	# The IPs are differnt!

	# Call the API
	# TO DO: ADD THE API CALL!!!

	# Update $IPSaveLocation
	echo "$currentExtIP" > "$IPSaveLocation"

	echo "IP Updated"

fi

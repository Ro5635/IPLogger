 #!/bin/bash 

# This checks the current IP Address and compares it with the IP address that was used in the
# last update, if it has changed it calls the API and updates the IP address and saves the 
# updated value to the file specified IPSaveLocation.
# This script should be executed at an interval (10 mins?) on the remote PC Whose IP is to be
# tracked.

# Location to save the last IP
IPSaveLocation=/tmp/IPTracker
IPTrackerURL=http://127.0.0.1:5000

# Get the current External IP address
currentExtIP=$(dig +short myip.opendns.com @resolver1.opendns.com)

# Check to see if this IP is the same as the last submitted IP
lastSubmittedIP=$(cat $IPSaveLocation/LastIP)

echo "The last IP: $lastSubmittedIP"

echo "Current IP: $currentExtIP"


# Has the IP changed since the last update?
if [ "$lastSubmittedIP" == "$currentExtIP" ]; then
	# The IP is the same!

	# Nothing to do, exit.
	echo "IP Unchanged"
else
	# The IPs are differnt!
	# get the priv_key and Remote_ID
	Remote_ID=$(cat $IPSaveLocation/Remote_ID)
	Priv_Key=$(cat $IPSaveLocation/Priv_Key)


	# Call the API
	curl  -H "Content-Type: application/json" -X POST -d '{"id_number":"'"$Remote_ID"'", "priv_key":"'"$Priv_Key"'"}' -i $IPTrackerURL/update 

	# Update $IPSaveLocation
	echo "$currentExtIP" > "$IPSaveLocation/LastIP"

	echo " IP Updated"

fi

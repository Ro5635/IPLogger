from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import json
from flask import jsonify
import random

"""
My DDNS Service with noip.com expired 15 minutes ago. Things are breaking, this is a stop gap solution to be applied to
 my home servers to log their IP.
 
 Robert Curran 2017

"""

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations; I have been developing with the DB and web server on separate Docker containers, as such details
# are needed as below. Replace with your mysql servers details.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '5635'
app.config['MYSQL_DATABASE_DB'] = 'ServerLogging'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.3'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/ips')
def ips():
    """
    This outputs all of the Server IPS that are currently stored in the system out to the page
     
    """
    # Connect to the DB and get all of the server connections:
    cursor.execute("SELECT CurrentAddress_IP , CurrentAddress_Last_Update , Remote_Registration_Date,"
                   " Remotes.Remote_ID, Remote_Name FROM Remotes, CurrentAddress "
                   "WHERE Remotes.Remote_ID = CurrentAddress.Remote_ID LIMIT 250;")

    all_servers = cursor.fetchall()

    # Pass the DB data over to the template
    return render_template('servers.html', all_servers=all_servers)


@app.route('/update', methods=['POST'])
def update():
    """
    TODO: Add some kind of security/verification
    
    :return: 
    """
    # Load the received JSON data
    content = (request.get_json())
    # json.loads
    _idNumber = content['id_number']

    trusted_proxies = {'127.0.0.1'}  # Local Proxy of apache/Nginx expected
    route = request.access_route + [request.remote_addr]

    # Get the IP from the forward header, ensure that the proxy is white listed for security.
    _ip = next((addr for addr in reversed(route)
                        if addr not in trusted_proxies), request.remote_addr)

    # _ip = request.remote_addr

    _priv_key = content['priv_key']

    if _idNumber and _priv_key:
        # if the key and ID are correct update
        try:
            cursor.execute("UPDATE CurrentAddress JOIN Remotes on CurrentAddress.Remote_ID = Remotes.Remote_ID "
                           "SET CurrentAddress_IP = %s WHERE Remote_PrivKey = %s AND Remotes.Remote_ID = %s;"
                           , (_ip, _priv_key, _idNumber,))

            if cursor.rowcount == 1:
                # Its safe to Commit Changes as we expect 1 row change
                conn.commit()
            elif cursor.rowcount == 0:
                # The IP was all ready up to date, no changes made. commit.
                conn.commit()
            else:
                raise IndexError("Unexpected number of Rows were mutated by DB insertion")

        except IndexError as error:
            print("Insert Failed, Reason: ", error.message)

        # Return successful update status
        return json.dumps({'status': 200})
    else:
        return json.dumps({'status': 400, 'error': 'Required fields were missing', 'received': content})


@app.route('/newserver', methods=['POST'])
def newserver():
    """
    Create a new Server to be tracked
    Some rate limiting on this endpoint would be good...
    
    :return: New Server ID and Private "Key"
    """

    # Extract the new remotes name from the request, this need not be unique
    request_content = request.get_json()
    _requesting_IP = request.remote_addr

    _new_name = request_content['remote_name']

    # Get a new ID

    # Run at least once
    found_remotes = []
    _potential_new_ID = 0

    # Switch this to a for and throw exception if to many attempts..
    while len(found_remotes) > 0 or _potential_new_ID <= 0:
        _potential_new_ID = random.randint(10000, 9999999)

        # Check that the ID is not all ready in use:
        cursor.execute("SELECT Remote_ID FROM Remotes WHERE Remote_ID = %s", _potential_new_ID)
        found_remotes = cursor.fetchall()

        len(found_remotes)

    _new_ID = _potential_new_ID
    #  Generate new Key

    # Not really a key, but this will hold for now
    new_priv_key = random.getrandbits(256)

    try:
        #  Add new Remote to the DB
        cursor.execute("INSERT INTO Remotes(Remote_ID, Remote_Name, Remote_PrivKey) VALUES(%s, %s, %s);",
                       (_new_ID, _new_name, new_priv_key,))

        if cursor.rowcount == 1:
            # Its safe to Commit Changes
            conn.commit()
        else:
            raise IndexError("Unexpected number of Rows were mutated by DB insertion")
    except IndexError as error:
        print("Insert Failed, Reason: ", error.message)

    # Prepare the Addresses table with this new Remote, use the requests origin IP as the initial value
    try:
        cursor.execute("INSERT INTO CurrentAddress(Remote_ID, CurrentAddress_IP) VALUES(%s , %s);", (_new_ID, _requesting_IP))

        if cursor.rowcount == 1:
            # Its safe to Commit Changes
            conn.commit()
        else:
            raise IndexError("Unexpected Number of rows Mutated by DB Insertion")

    except IndexError as error:
        print("The Insert into currentAddress Failed, reason: ", error.message)

    #  Return the new ID and Private Key
    return_data = json.dumps({'remote_name': _new_name, 'remote_id': _new_ID, 'new_priv_key': str(new_priv_key)})

    return jsonify(return_data)


if __name__ == "__main__":
    app.run()

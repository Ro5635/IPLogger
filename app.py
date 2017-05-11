from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import json

"""
My DDNS Service with noip.com expired 15 minutes ago. Things are breaking, this is a stop gap solution to be applied to
 my home servers to log their IP.
 
 Robert Curran 2017

"""

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '5635'
app.config['MYSQL_DATABASE_DB'] = 'ServerLogging'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.2'
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
    cursor.execute("SELECT id, ipaddress, name, lastmodified FROM Servers")
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
    content = json.loads(request.get_json())

    _idNumber = content['id_number']
    _ip = request.remote_addr

    # validate the received values
    if _idNumber:

        cursor.execute("UPDATE Servers SET ipaddress = %s WHERE id = %s", (_ip, _idNumber,))

        conn.commit()

        return json.dumps({'status': 200})
    else:
        return json.dumps({'status': 400, 'error': 'Required fields were missing'})


if __name__ == "__main__":
    app.run()

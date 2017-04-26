from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import json

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


@app.route('/update', methods=['POST'])
def update():
    # Load the received JSON data
    content = json.loads(request.get_json())

    _idNumber = content['id_number']
    _ip = request.remote_addr

    # validate the received values
    if _idNumber:

        cursor.execute("UPDATE Servers SET ipaddress = %s WHERE id = %s", (_ip, _idNumber,))

        cursor.execute("SELECT * FROM Servers")
        data = cursor.fetchone()

        conn.commit()

        return json.dumps({'status': 200})
    else:
        return json.dumps({'status': 400, 'error': 'Required fields were missing'})


if __name__ == "__main__":
    app.run()

from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "Lenovo"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "Company"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query, values=None):
    cur = mysql.connection.cursor()
    if values:
        cur.execute(query, values)
    else:
        cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/employee", methods=["GET"])
def get_employee():
    data = data_fetch("""SELECT * FROM employee""")
    return make_response(jsonify(data), 200)

@app.route("/employee/<int:ssn>", methods=["GET"])
def get_employee_by_ssn(ssn):
    data = data_fetch("SELECT * FROM employee WHERE ssn = %s", (ssn,))
    return make_response(jsonify(data), 200)

@app.route("/employee", methods=["POST"])
def add_employee():
    cur = mysql.connection.cursor()
    info = request.get_json()
    fname =info["first_name"]
    lname = info["last_name"]
    cur.execute(
        """ INSERT INTO employee (first_name, last_name) Value (%s, %s)""", (fname, lname),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "employee added succesfully", "rows_affected": cur.rowcount}), 200)


if __name__ == "__main__":
    app.run(debug=True)

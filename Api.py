from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "Lenovo"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "Company"

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/employee", methods=["GET"])
def get_employee():
    cur = mysql.connection.cursor()
    query = """
    SELECT * FROM employee
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)

@app.route("/employee/<int:ssn>",methods=["GET"])
def get_employee_by_ssn(ssn):
    cur = mysql.connection.cursor()
    query = """
    SELECT * FROM employee where ssn = {}
    """.format(ssn)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

if __name__ == "__main__":
    app.run(debug=True)

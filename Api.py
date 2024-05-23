from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MySQL_HOST"] = "localhost"
app.config["MySQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MSQL_DB"] = "Company"

app.config['MSQL_CURSOCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/employee", methods=["GET"])
def get_actors():
    cur = mysql.connection.cursor()
    query = """
    select * from employee
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close

    return make_response(jsonify(data), 200)


if __name__ == "__main__":
    app.run(debug=True)
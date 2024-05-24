from flask import Flask, make_response, jsonify, request, render_template_string
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "Lenovo"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "Company"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def data_fetch(query, values=None):
    cur = mysql.connection.cursor()
    if values:
        cur.execute(query, values)
    else:
        cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def home_screen():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Management</title>
</head>
<body>
<header>
    <h1>Employee Management System</h1>
</header>
<section id="employee-section">
    <h2>List of Employees</h2>
    <button id="view-employee-btn">View Employee</button>
</section>
<script>
    document.getElementById("view-employee-btn").addEventListener("click", function() {
        window.location.href = "/employee";
    });
</script>
</body>
</html>
""")

@app.route("/employee", methods=["GET"])
def get_employee():
    query = "SELECT * FROM employee"
    employees = data_fetch(query)
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Information</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Employee Information</h1>
    <button id="return-home-btn">Return to Home</button>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Address</th>
                <th>Birthdate</th>
                <th>Driver's License ID</th>
                <th>Salary</th>
                <th>Sex</th>
                <th>Supervisor SSN</th>
                <th>SSN</th>
            </tr>
        </thead>
        <tbody>
            {% for employee in employees %}
            <tr>
                <td>{{ employee.Fname }} {{ employee.Minit }} {{ employee.Lname }}</td>
                <td>{{ employee.Address }}</td>
                <td>{{ employee.Bdate }}</td>
                <td>{{ employee.DL_id }}</td>
                <td>${{ employee.Salary }}</td>
                <td>{{ employee.Sex }}</td>
                <td>{{ employee.Super_ssn or "None" }}</td>
                <td>{{ employee.ssn }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <script>
        document.getElementById("return-home-btn").addEventListener("click", function() {
            window.location.href = "/";
        });
    </script>
</body>
</html>
""", employees=employees)

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
    return make_response(jsonify({"message": "employee added successfully", "rows_affected": cur.rowcount}), 200)

@app.route("/employee/<int:ssn>", methods=["Put"])
def update_employee(ssn):
    cur = mysql.connection.cursor()
    info = request.get_json()
    fname = info["first_name"]
    lname = info["last_name"]
    cur.execute("""
    UPDATE employee Set first_name = %s, last_name = %s Where employee_id = %s""", 
    (fname, lname, ssn),)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "employee updated successfully", "rows_affected": rows_affected}), 200)

@app.route("/employee/<int:ssn>", methods=["DELETE"])
def delete_employee(ssn):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE form employee where ssn = %s""", (ssn))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "employee deleted successfully", "rows_affected": rows_affected}), 200)

@app.route("/employee/format", methods=["GET"])
def get_params():
    fmt = request.args.get("ssn")
    foo = request.args.get("aaaa")
    return make_response(jsonify({"format": fmt, "foo":foo}, 200))


if __name__ == "__main__":
    app.run(debug=True)

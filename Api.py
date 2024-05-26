from flask import Flask, jsonify, render_template_string, request, redirect, url_for, flash, Response
from flask_mysqldb import MySQL
import xmltodict

app = Flask(__name__)
app.config.update(
    MYSQL_HOST="localhost",
    MYSQL_USER="Lenovo",
    MYSQL_PASSWORD="root",
    MYSQL_DB="Company",
    MYSQL_CURSORCLASS="DictCursor",
    SECRET_KEY="your_secret_key"
)

mysql = MySQL(app)

def execute_query(query, values=None, fetch=False):
    cur = mysql.connection.cursor()
    cur.execute(query, values or ())
    if fetch:
        result = cur.fetchall()
    else:
        mysql.connection.commit()
        result = None
    cur.close()
    return result

def format_response(data, response_format):
    if response_format == "xml":
        xml = xmltodict.unparse({"root": data})
        return Response(xml, mimetype='application/xml')
    return jsonify(data)

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
        <button onclick="location.href='/employee'">View Employees</button>
        <h3>Add a New Employee</h3>
        <button onclick="location.href='/add_employee'">Add Employee</button>
        <h3>Update an Employee</h3>
        <button onclick="location.href='/update_employee'">Update Employee</button>
        <h3>Delete an Employee</h3>
        <button onclick="location.href='/delete_employee'">Delete Employee</button>
    </section>
</body>
</html>
""")

@app.route("/employee", methods=["GET"])
def get_employee():
    employees = execute_query("SELECT * FROM employee", fetch=True)
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Information</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Employee Information</h1>
    <button onclick="location.href='/'">Return to Home</button>
    <table>
        <thead>
            <tr>
                <th>Name</th><th>Address</th><th>Birthdate</th><th>Department Location ID</th>
                <th>Salary</th><th>Sex</th><th>Supervisor SSN</th><th>SSN</th>
            </tr>
        </thead>
        <tbody>
            {% for emp in employees %}
            <tr>
                <td>{{ emp.Fname }} {{ emp.Minit }} {{ emp.Lname }}</td>
                <td>{{ emp.Address }}</td><td>{{ emp.Bdate }}</td>
                <td>{{ emp.DL_id }}</td><td>${{ emp.Salary }}</td>
                <td>{{ emp.Sex }}</td><td>{{ emp.Super_ssn or "None" }}</td><td>{{ emp.ssn }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
""", employees=employees)

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        data = {field: request.form[field] for field in request.form}
        errors = []

        if not data["Fname"].isalpha():
            errors.append("First Name must be letters only.")
        if not data["Minit"].isalpha() or len(data["Minit"]) != 1:
            errors.append("Middle Initial must be a single letter.")
        if not data["Lname"].isalpha():
            errors.append("Last Name must be letters only.")
        if not data["DL_id"].isdigit():
            errors.append("Department Location ID must be a number.")
        if not data["Salary"].isdigit():
            errors.append("Salary must be a number.")
        if data["Sex"] not in ["M", "F"]:
            errors.append("Sex must be either 'M' or 'F'.")
        if not data["Super_ssn"].isdigit():
            errors.append("Supervisor SSN must be a number.")
        if not data["ssn"].isdigit() or len(data["ssn"]) != 9:
            errors.append("SSN must be a 9-digit number.")

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for("add_employee"))

        query = """INSERT INTO employee (Fname, Minit, Lname, Address, Bdate, DL_id, Salary, Sex, Super_ssn, ssn)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_query(query, (data["Fname"], data["Minit"], data["Lname"], data["Address"], data["Bdate"], data["DL_id"], data["Salary"], data["Sex"], data["Super_ssn"], data["ssn"]))
        return redirect(url_for("get_employee"))

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Employee</title>
    <script>
        function validateForm() {
            var Fname = document.forms["employeeForm"]["Fname"].value;
            var Minit = document.forms["employeeForm"]["Minit"].value;
            var Lname = document.forms["employeeForm"]["Lname"].value;
            var Address = document.forms["employeeForm"]["Address"].value;
            var Bdate = document.forms["employeeForm"]["Bdate"].value;
            var DL_id = document.forms["employeeForm"]["DL_id"].value;
            var Salary = document.forms["employeeForm"]["Salary"].value;
            var Sex = document.forms["employeeForm"]["Sex"].value;
            var Super_ssn = document.forms["employeeForm"]["Super_ssn"].value;
            var ssn = document.forms["employeeForm"]["ssn"].value;

            if (!Fname.match(/^[a-zA-Z]+$/)) {
                alert("First Name must be letters only.");
                return false;
            }
            if (!Minit.match(/^[a-zA-Z]$/)) {
                alert("Middle Initial must be a single letter.");
                return false;
            }
            if (!Lname.match(/^[a-zA-Z]+$/)) {
                alert("Last Name must be letters only.");
                return false;
            }
            if (Address === "") {
                alert("Address must not be blank.");
                return false;
            }
            if (Bdate === "") {
                alert("Birthdate must not be blank.");
                return false;
            }
            if (!DL_id.match(/^[0-9]+$/)) {
                alert("Department Location ID must be a number.");
                return false;
            }
            if (!Salary.match(/^[0-9]+$/)) {
                alert("Salary must be a number.");
                return false;
            }
            if (Sex !== "M" && Sex !== "F") {
                alert("Sex must be either 'M' or 'F'.");
                return false;
            }
            if (!Super_ssn.match(/^[0-9]+$/)) {
                alert("Supervisor SSN must be a number.");
                return false;
            }
            if (!ssn.match(/^[0-9]{9}$/)) {
                alert("SSN must be a 9-digit number.");
                return false;
            }
            return true;
        }
    </script>
</head>
<body>
    <h1>Add a New Employee</h1>
    <form name="employeeForm" action="/add_employee" method="post" onsubmit="return validateForm()">
        <label for="fname">First Name:</label><input type="text" id="fname" name="Fname"><br>
        <label for="minit">Middle Initial:</label><input type="text" id="minit" name="Minit"><br>
        <label for="lname">Last Name:</label><input type="text" id="lname" name="Lname"><br>
        <label for="address">Address:</label><input type="text" id="address" name="Address"><br>
        <label for="bdate">Birthdate:</label><input type="date" id="bdate" name="Bdate"><br>
        <label for="dl_id">Department Location ID:</label><input type="text" id="dl_id" name="DL_id"><br>
        <label for="salary">Salary:</label><input type="text" id="salary" name="Salary"><br>
        <label for="sex">Sex:</label><input type="text" id="sex" name="Sex"><br>
        <label for="super_ssn">Supervisor SSN:</label><input type="text" id="super_ssn" name="Super_ssn"><br>
        <label for="ssn">SSN:</label><input type="text" id="ssn" name="ssn"><br>
        <input type="submit" value="Submit">
    </form>
    <button onclick="location.href='/'">Return to Home</button>
</body>
</html>
""")

@app.route("/update_employee", methods=["GET", "POST"])
def update_employee():
    if request.method == "POST":
        ssn = request.form.get("ssn")
        if not ssn:
            flash("SSN is required.")
            return redirect(url_for("update_employee"))

        if "update_details" in request.form:
            data = request.form
            query = """
            UPDATE employee 
            SET Fname = %s, Minit = %s, Lname = %s, Address = %s, Bdate = %s, DL_id = %s, Salary = %s, Sex = %s, Super_ssn = %s 
            WHERE ssn = %s
            """
            execute_query(query, (data["fname"], data["minit"], data["lname"], data["address"], data["bdate"], data["dl_id"], data["salary"], data["sex"], data["super_ssn"], ssn))
            return redirect(url_for("get_employee"))

        employee = execute_query("SELECT * FROM employee WHERE ssn = %s", (ssn,), fetch=True)
        if not employee:
            flash(f"Employee with SSN {ssn} does not exist.")
            return redirect(url_for("update_employee"))

        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Update Employee</title></head>
<body>
<h1>Update Employee</h1>
<form action="/update_employee" method="post">
    <input type="hidden" name="ssn" value="{{ employee[0].ssn }}">
    <label for="fname">First Name:</label><br><input type="text" id="fname" name="fname" value="{{ employee[0].Fname }}"><br>
    <label for="minit">Middle Initial:</label><br><input type="text" id="minit" name="minit" value="{{ employee[0].Minit }}"><br>
    <label for="lname">Last Name:</label><br><input type="text" id="lname" name="lname" value="{{ employee[0].Lname }}"><br>
    <label for="address">Address:</label><br><input type="text" id="address" name="address" value="{{ employee[0].Address }}"><br>
    <label for="bdate">Birthdate:</label><br><input type="date" id="bdate" name="bdate" value="{{ employee[0].Bdate }}"><br>
    <label for="dl_id">Department Location ID:</label><br><input type="text" id="dl_id" name="dl_id" value="{{ employee[0].DL_id }}"><br>
    <label for="salary">Salary:</label><br><input type="number" id="salary" name="salary" value="{{ employee[0].Salary }}"><br>
    <label for="sex">Sex:</label><br><input type="text" id="sex" name="sex" value="{{ employee[0].Sex }}"><br>
    <label for="super_ssn">Supervisor SSN:</label><br><input type="text" id="super_ssn" name="super_ssn" value="{{ employee[0].Super_ssn }}"><br>
    <input type="submit" name="update_details" value="Update Employee">
</form>
<button onclick="window.location.href='/'">Return to Home</button>
</body>
</html>
""", employee=employee)

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Update Employee</title></head>
<body>
<h1>Update Employee</h1>
<form action="/update_employee" method="post">
    <label for="ssn">Enter SSN of the Employee to Update:</label><br><input type="text" id="ssn" name="ssn"><br>
    <input type="submit" value="Get Employee Details">
</form>
<button onclick="window.location.href='/'">Return to Home</button>
</body>
</html>
""")

@app.route("/delete_employee", methods=["GET", "POST"])
def delete_employee():
    if request.method == "POST":
        ssn = request.form["ssn"]
        if not ssn.isdigit() or len(ssn) != 9:
            flash("SSN must be a 9-digit number.")
            return redirect(url_for("delete_employee"))

        existing_employee = execute_query("SELECT * FROM employee WHERE ssn = %s", (ssn,), fetch=True)
        if not existing_employee:
            flash("Employee with this SSN does not exist.")
            return redirect(url_for("delete_employee"))

        execute_query("DELETE FROM employee WHERE ssn = %s", (ssn,))
        return redirect(url_for("get_employee"))

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete Employee</title>
</head>
<body>
    <h1>Delete Employee</h1>
    <form action="/delete_employee" method="post">
        <label for="ssn">Employee SSN:</label><input type="text" id="ssn" name="ssn" required><br>
        <input type="submit" value="Delete">
    </form>
    <button onclick="location.href='/'">Return to Home</button>
</body>
</html>
""")

@app.route("/api/employee/<int:ssn>", methods=["GET"])
def api_get_employee(ssn):
    employee = execute_query("SELECT * FROM employee WHERE ssn = %s", (ssn,), fetch=True)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    return format_response(employee[0], request.args.get("format", "json"))

@app.route("/api/employee", methods=["POST"])
def api_add_employee():
    data = request.get_json()
    query = """INSERT INTO employee (Fname, Minit, Lname, Address, Bdate, DL_id, Salary, Sex, Super_ssn, ssn)
               VALUES (%(Fname)s, %(Minit)s, %(Lname)s, %(Address)s, %(Bdate)s, %(DL_id)s, %(Salary)s, %(Sex)s, %(Super_ssn)s, %(ssn)s)"""
    execute_query(query, data)
    return jsonify({"message": "Employee added successfully"}), 201

@app.route("/api/employee/<int:ssn>", methods=["PUT"])
def api_update_employee(ssn):
    data = request.get_json()
    updates = ", ".join([f"{k} = %s" for k in data.keys()])
    query = f"UPDATE employee SET {updates} WHERE ssn = %s"
    execute_query(query, (*data.values(), ssn))
    return jsonify({"message": "Employee updated successfully"})

@app.route("/api/employee/<int:ssn>", methods=["DELETE"])
def api_delete_employee(ssn):
    execute_query("DELETE FROM employee WHERE ssn = %s", (ssn,))
    return jsonify({"message": "Employee deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)

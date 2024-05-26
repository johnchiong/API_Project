from flask import Flask, make_response, jsonify, request, render_template_string, redirect, url_for, flash
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

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        fname = request.form["fname"]
        minit = request.form["minit"]
        lname = request.form["lname"]
        address = request.form["address"]
        bdate = request.form["bdate"]
        dl_id = request.form["dl_id"]
        salary = request.form["salary"]
        sex = request.form["sex"]
        super_ssn = request.form["super_ssn"]
        ssn = request.form["ssn"]

        query = """
        INSERT INTO employee (Fname, Minit, Lname, Address, Bdate, DL_id, Salary, Sex, Super_ssn, ssn)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (fname, minit, lname, address, bdate, dl_id, salary, sex, super_ssn, ssn)
        cur = mysql.connection.cursor()
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for("get_employee"))
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Employee</title>
</head>
<body>
    <h1>Add an Employee</h1>
    <form action="/add_employee" method="post">
        <label for="fname">First Name:</label><br>
        <input type="text" id="fname" name="fname"><br>
        <label for="minit">Middle Initial:</label><br>
        <input type="text" id="minit" name="minit"><br>
        <label for="lname">Last Name:</label><br>
        <input type="text" id="lname" name="lname"><br>
        <label for="address">Address:</label><br>
        <input type="text" id="address" name="address"><br>
        <label for="bdate">Birthdate:</label><br>
        <input type="date" id="bdate" name="bdate"><br>
        <label for="dl_id">Department Location ID:</label><br>
        <input type="text" id="dl_id" name="dl_id"><br>
        <label for="salary">Salary:</label><br>
        <input type="number" id="salary" name="salary"><br>
        <label for="sex">Sex:</label><br>
        <input type="text" id="sex" name="sex"><br>
        <label for="super_ssn">Supervisor SSN:</label><br>
        <input type="text" id="super_ssn" name="super_ssn"><br>
        <label for="ssn">SSN:</label><br>
        <input type="text" id="ssn" name="ssn"><br>
        <input type="submit" value="Add Employee">
    </form>
    <button id="return-home-btn">Return to Home</button>
    <script>
        document.getElementById("return-home-btn").addEventListener("click", function() {
            window.location.href = "/";
        });
    </script>
</body>
</html>
""")

@app.route("/update_employee", methods=["GET", "POST"])
def update_employee():
    if request.method == "POST":
        ssn = request.form["ssn"]
        query = "SELECT * FROM employee WHERE ssn = %s"
        employee = data_fetch(query, (ssn,))
        
        if not employee:
            flash("Employee with SSN {} does not exist.".format(ssn))
            return redirect(url_for("update_employee"))
        
        employee = employee[0]
        
        if "update_details" in request.form:
            fname = request.form["fname"]
            minit = request.form["minit"]
            lname = request.form["lname"]
            address = request.form["address"]
            bdate = request.form["bdate"]
            dl_id = request.form["dl_id"]
            salary = request.form["salary"]
            sex = request.form["sex"]
            super_ssn = request.form["super_ssn"]

            query = """
            UPDATE employee 
            SET Fname = %s, Minit = %s, Lname = %s, Address = %s, Bdate = %s, DL_id = %s, Salary = %s, Sex = %s, Super_ssn = %s 
            WHERE ssn = %s
            """
            values = (fname, minit, lname, address, bdate, dl_id, salary, sex, super_ssn, ssn)
            cur = mysql.connection.cursor()
            cur.execute(query, values)
            mysql.connection.commit()
            cur.close()

            return redirect(url_for("get_employee"))
        
        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Employee</title>
</head>
<body>
    <h1>Update Employee</h1>
    <form action="/update_employee" method="post">
        <input type="hidden" name="ssn" value="{{ employee.ssn }}">
        <label for="fname">First Name:</label><br>
        <input type="text" id="fname" name="fname" value="{{ employee.Fname }}"><br>
        <label for="minit">Middle Initial:</label><br>
        <input type="text" id="minit" name="minit" value="{{ employee.Minit }}"><br>
        <label for="lname">Last Name:</label><br>
        <input type="text" id="lname" name="lname" value="{{ employee.Lname }}"><br>
        <label for="address">Address:</label><br>
        <input type="text" id="address" name="address" value="{{ employee.Address }}"><br>
        <label for="bdate">Birthdate:</label><br>
        <input type="date" id="bdate" name="bdate" value="{{ employee.Bdate }}"><br>
        <label for="dl_id">Department Location ID:</label><br>
        <input type="text" id="dl_id" name="dl_id" value="{{ employee.DL_id }}"><br>
        <label for="salary">Salary:</label><br>
        <input type="number" id="salary" name="salary" value="{{ employee.Salary }}"><br>
        <label for="sex">Sex:</label><br>
        <input type="text" id="sex" name="sex" value="{{ employee.Sex }}"><br>
        <label for="super_ssn">Supervisor SSN:</label><br>
        <input type="text" id="super_ssn" name="super_ssn" value="{{ employee.Super_ssn }}"><br>
        <input type="submit" name="update_details" value="Update Employee">
    </form>
    <button id="return-home-btn">Return to Home</button>
    <script>
        document.getElementById("return-home-btn").addEventListener("click", function() {
            window.location.href = "/";
        });
    </script>
</body>
</html>
""", employee=employee)

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Employee</title>
</head>
<body>
    <h1>Update Employee</h1>
    <form action="/update_employee" method="post">
        <label for="ssn">Enter Employee SSN:</label><br>
        <input type="text" id="ssn" name="ssn"><br>
        <input type="submit" value="Find Employee">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <button id="return-home-btn">Return to Home</button>
    <script>
        document.getElementById("return-home-btn").addEventListener("click", function() {
            window.location.href = "/";
        });
    </script>
</body>
</html>
""")

@app.route("/delete_employee", methods=["GET", "POST"])
def delete_employee():
    if request.method == "POST":
        ssn = request.form["ssn"]
        query = "SELECT * FROM employee WHERE ssn = %s"
        employee = data_fetch(query, (ssn,))
        
        if not employee:
            flash("Employee with SSN {} does not exist.".format(ssn))
            return redirect(url_for("delete_employee"))

        query = "DELETE FROM employee WHERE ssn = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (ssn,))
        mysql.connection.commit()
        cur.close()

        flash("Employee with SSN {} has been deleted.".format(ssn))
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
        <label for="ssn">Enter Employee SSN:</label><br>
        <input type="text" id="ssn" name="ssn"><br>
        <input type="submit" value="Delete Employee">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <button id="return-home-btn">Return to Home</button>
    <script>
        document.getElementById("return-home-btn").addEventListener("click", function() {
            window.location.href = "/";
        });
    </script>
</body>
</html>
""")

if __name__ == "__main__":
    app.run(debug=True)

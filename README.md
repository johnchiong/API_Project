Employee Management System
This is a Flask-based web application for managing employees in a company. It supports CRUD (Create, Read, Update, Delete) operations and offers both a web interface and a REST API.

Features
View list of employees
Add a new employee
Update an existing employee's details
Delete an employee
REST API for managing employees programmatically

Requirements
Python 3.x
Flask
Flask-MySQLdb
xmltodict

Installation

1. Clone the repository:
git clone https://github.com/yourusername/employee-management-system.git
cd employee-management-system

2. Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate

3. Install the required packages:
pip install Flask, Flask-MySQLdb, and xmltodict

3. Configure MySQL database connection in 'app.config'
app.config.update(
    MYSQL_HOST="localhost",
    MYSQL_USER="your_mysql_username",
    MYSQL_PASSWORD="your_mysql_password",
    MYSQL_DB="your_database_name",
    MYSQL_CURSORCLASS="DictCursor",
    SECRET_KEY="your_secret_key"
)

4. Create the employee table in your MySQL database:
CREATE TABLE employee (
    Fname VARCHAR(50),
    Minit CHAR(1),
    Lname VARCHAR(50),
    Address VARCHAR(100),
    Bdate DATE,
    DL_id INT,
    Salary DECIMAL(10, 2),
    Sex CHAR(1),
    Super_ssn VARCHAR(9),
    ssn VARCHAR(9) PRIMARY KEY
);
Running the Application

5. Run the Flask application:
flask run

Open your web browser and navigate to http://localhost:5000 to access the application.
Remember that the other devices must be connected on the same network, either LAN or wireless.

Usage
Once the application is running, you can perform the following actions:

Add a new employee
View all employees
Update an existing employee
Delete an employee
View employees in JSON or XML format

API Endpoints

Get Employee Details
URL: '/api/employee/<ssn>'
Method: 'GET'
Query Parameter: 'format (optional, values: json or xml)'

Add a New Employee
URL: '/api/employee'
Method: 'POST'
Body: 'JSON object with employee details'

Update an Employee
URL: '/api/employee/<ssn>'
Method: 'PUT'
Body: 'JSON object with updated employee details'

Delete an Employee
URL: '/api/employee/<ssn>'
Method: 'DELETE'

Additional Information
	This project is for educational purposes and may not be suitable for production use without further enhancements.
	Contributions are welcome. Feel free to submit issues or pull requests.
	Note: If you encounter issues with the code not recognizing the installed libraries after installing the dependencies from 				
 	requirements.txt, try reinstalling the libraries and restarting your code editor or IDE (e.g., VSCode).

import unittest
import warnings
from Api import app, mysql

class EmployeeTests(unittest.TestCase):
    def setUp(self):
        # Create an application context
        self.app_context = app.app_context()
        self.app_context.push()

        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()

        # Create a test database context
        self.connection = mysql.connect
        self.cursor = self.connection.cursor()
        
        # Add a test employee to the database for testing purposes
        self.cursor.execute("""
        INSERT INTO employee (Fname, Minit, Lname, Address, Bdate, DL_id, Salary, Sex, Super_ssn, ssn) 
        VALUES ('Test', 'T', 'User', '123 Test St', '1990-01-01', '1', '50000', 'M', '987654321', '123455778')
        """)
        self.connection.commit()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def tearDown(self):
        # Remove the test employee from the database
        self.cursor.execute("DELETE FROM employee WHERE ssn = '123455778'")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

        # Remove the application context
        self.app_context.pop()

    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Employee Management System", response.data.decode())

    def test_get_employees(self):
        response = self.app.get("/api/employee")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test User", response.data.decode())

    def test_get_employee_by_ssn(self):
        response = self.app.get("/api/employee/123455778")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test", response.data.decode())

    def test_add_employee(self):
        response = self.app.post("/api/employee", json={
            "Fname": "Jane",
            "Minit": "D",
            "Lname": "Doe",
            "Address": "456 New St",
            "Bdate": "1985-05-05",
            "DL_id": 2,
            "Salary": 60000,
            "Sex": "F",
            "Super_ssn": "987654321",
            "ssn": "9876543210"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_employee(self):
        response = self.app.put("/api/employee/123455778", json={
            "Fname": "Updated",
            "Minit": "U",
            "Lname": "User",
            "Address": "123 Updated St",
            "Bdate": "1990-01-01",
            "DL_id": 1,
            "Salary": 55000,
            "Sex": "M",
            "Super_ssn": "987654321"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Employee updated successfully", response.data.decode())

    def test_delete_employee(self):
        response = self.app.delete("/api/employee/123455778")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Test User", response.data.decode())

if __name__ == "__main__":
    unittest.main()

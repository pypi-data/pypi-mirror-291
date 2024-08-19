# varsync/varsync.py

import json
import mysql.connector

class VSyncSession:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.conn = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="sql12726531",
            password="r5xy72c5Yk",
            database="sql12726531"
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self._authenticate()

    def _authenticate(self):
        query = "SELECT * FROM user WHERE UserName = %s AND Password = %s"
        self.cursor.execute(query, (self.username, self.password))
        user = self.cursor.fetchone()
        if not user:
            raise ValueError("Invalid credentials")
        self.variables = json.loads(user['Variables']) if user['Variables'] else {}

    def get(self, var_name):
        return self.variables.get(var_name, "Variable not set")

    def create(self, var_name, var_value):
        if var_name in self.variables:
            return "Variable exists already. Use edit() to edit the value of the variable"
        self.variables[var_name] = var_value
        self._update_db()

    def edit(self, var_name, var_value):
        if var_name not in self.variables:
            return "Variable not set. Use create() to create a new variable"
        self.variables[var_name] = var_value
        self._update_db()

    def delete(self, var_name):
        if var_name not in self.variables:
            return "Variable not set"
        del self.variables[var_name]
        self._update_db()

    def list(self):
        return self.variables

    def _update_db(self):
        variables_json = json.dumps(self.variables)
        query = "UPDATE user SET Variables = %s WHERE UserName = %s"
        self.cursor.execute(query, (variables_json, self.username))
        self.conn.commit()

def login(username, password):
    return VSyncSession(username, password)

def register(username, password, confirm_password):
    if password != confirm_password:
        raise ValueError("Passwords do not match")
    conn = mysql.connector.connect(
        host="sql12.freemysqlhosting.net",
        user="sql12726531",
        password="r5xy72c5Yk",
        database="sql12726531"
    )
    cursor = conn.cursor()
    query = "INSERT INTO user (UserName, Password, Variables) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (username, password, json.dumps({})))
        conn.commit()
    except mysql.connector.IntegrityError:
        raise ValueError("Username already exists")
    finally:
        cursor.close()
        conn.close()

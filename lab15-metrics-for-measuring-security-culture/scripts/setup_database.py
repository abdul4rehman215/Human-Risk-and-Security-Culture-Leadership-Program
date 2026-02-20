import sqlite3


def create_database():
    """
    Create SQLite database with tables for security culture metrics.

    Tables:
    - employees (id, employee_id, department, role, hire_date)
    - security_training (id, employee_id, training_type, completion_date, score)
    - phishing_simulations (id, employee_id, simulation_date, clicked_link, reported_email)
    - security_incidents (id, employee_id, incident_date, incident_type, severity)
    - security_surveys (id, employee_id, survey_date, awareness_score, behavior_score)
    """
    conn = sqlite3.connect('data/security_culture.db')
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            hire_date TEXT NOT NULL
        );
    """)

    # Create security_training table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_training (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            training_type TEXT NOT NULL,
            completion_date TEXT NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
    """)

    # Create phishing_simulations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phishing_simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            simulation_date TEXT NOT NULL,
            clicked_link INTEGER NOT NULL CHECK(clicked_link IN (0,1)),
            reported_email INTEGER NOT NULL CHECK(reported_email IN (0,1)),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
    """)

    # Create security_incidents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            incident_date TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                ON UPDATE CASCADE
                ON DELETE SET NULL
        );
    """)

    # Create security_surveys table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_surveys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            survey_date TEXT NOT NULL,
            awareness_score INTEGER NOT NULL,
            behavior_score INTEGER NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database schema created at data/security_culture.db")

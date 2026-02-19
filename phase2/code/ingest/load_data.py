import pandas as pd
from db.connection import Neo4jConnection
from graph import schema
from models.employee import EmployeeModel

# Map CSV column headers to EmployeeModel field names
CSV_TO_MODEL = {
    "Name": "name",
    "Age": "age",
    "Gender": "gender",
    "Projects Completed": "project_completed",
    "Productivity (%)": "productivity",
    "Satisfaction Rate (%)": "satisfaction_rate",
    "Feedback Score": "feedback_score",
    "Department": "department",
    "Position": "position",
    "Joining Date": "joining_date",
    "Salary": "salary",
}


def ingest_employee(file_path: str):
    df = pd.read_csv(file_path)
    df = df.rename(columns=CSV_TO_MODEL)
    db = Neo4jConnection()

    for constraint in schema.CREATE_CONSTRAINTS:
        db.execute(constraint)

    for _, row in df.iterrows():
        try:
            employee = EmployeeModel(**row.to_dict())
        except Exception as e:
            print(f"Validation failed: {e}")
            continue

        data = employee.model_dump()
        db.execute(schema.CREATE_EMPLOYEE, data)
        db.execute(schema.CREATE_HAS_ROLE_REL, data)
        db.execute(schema.CREATE_WORKS_IN_REL, data)

    db.close()  

    
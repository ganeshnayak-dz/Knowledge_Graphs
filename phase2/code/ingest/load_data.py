import pandas as pd
from db.connection import Neo4jConnection
from graph import schema
from models import EmployeeModel



def ingest_employee(file_path:str):

    df=pd.read_csv(file_path)
    db=Neo4jConnection()

    for constraint in schema.CREATE_CONSTRAINS:
        db.execute(constraint)
    
    for _,row in df.iterrows():
        try:
            employee=EmployeeModel(**row.to_dict())
        except Exception as e:
            print(f"Validation failed:{e}")
            continue
    
        db.execute(schema.CREATE_EMPLOYEE,employee.model_dump())
        db.execute(schema.CREATE_HAS_ROLE_REL,employee.model_dump())
        db.execute(schema.CREATE_WORKS_IN_REL,employee.model_dump())

    db.close()  

    
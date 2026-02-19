from pydantic import BaseModel
from typing import Optional



class EmployeeModel(BaseModel):
    name:str
    age:int
    gender:str
    project_completed:int
    productivity:float
    satisfaction_rate:float
    feedback_score:int
    department:str
    postion:str
    joining_date:str
    salary:int
   

CREATE_CONSTRAINTS=["""
CREATE CONSTRAINT employee_name IF NOT EXISTS
FOR (e:Employee) REQUIRE e.name IS UNIQUE
""", """
CREATE CONSTRAINT department_unique IF NOT EXISTS
FOR (d:Department) REQUIRE d.department IS UNIQUE
""", """
CREATE CONSTRAINT position_unique IF NOT EXISTS
FOR (p:Position) REQUIRE p.position IS UNIQUE
"""]


CREATE_EMPLOYEE="""
MERGE (e:Employee {name: $name})
SET e.age = $age,
    e.gender = $gender,
    e.project_completed = $project_completed,
    e.productivity = $productivity,
    e.satisfaction_rate = $satisfaction_rate,
    e.feedback_score = $feedback_score,
    e.joining_date = $joining_date,
    e.salary = $salary
"""

CREATE_WORKS_IN_REL="""
MERGE (d:Department {department: $department})
WITH d
MATCH (e:Employee {name: $name})
MERGE (e)-[:WORKS_IN]->(d)
"""

CREATE_HAS_ROLE_REL="""
MERGE (p:Position {position: $position})
WITH p
MATCH (e:Employee {name: $name})
MERGE (e)-[:HAS_ROLE]->(p)
"""
from db.connection import Neo4jConnection

db = Neo4jConnection()

# get all movies
query1 = """
MATCH (m:Movie) RETURN  m.name, m.year
"""
result = db.execute_query(query1)
print("--------------------------------")
print("Query 1: Get all movies")
print("--------------------------------")
for row in result:
    print(dict(row))

print("--------------------------------")



db.close()


# import pandas as pd

# print("--------------------------------")
# employee_data = pd.read_csv(r'C:\WORK_DIR\Projects\Knowledge_graph\phase2\data\employee.csv')
# print("Employee Data:")
# print(employee_data.columns.tolist())
# print("--------------------------------")

from ingest.load_data import ingest_movies

if __name__=="__main__":
    ingest_movies(r"C:\WORK_DIR\Projects\Knowledge_graph\phase2\data\employee.csv")
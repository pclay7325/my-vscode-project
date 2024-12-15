import pandas as pd
import random
import datetime


# Define the columns for the work_orders table
columns = [
    "ID", "Operator", "Parent Order ID", "Material Definition ID", "Status", "Location", 
    "QTY Required", "QTY Complete", "QTY Scrap", "Due Date", "Start Date", "Complete Date", "Customer ID"
]

# Generate random data for the work_orders table
def generate_work_orders(rows=1000):
    statuses = ["CREATED", "RELEASED", "KITTED", "COMPLETED"]
    locations = ["Warehouse1", "Warehouse2", "Line1", "Line2"]
    operators = ["John Doe", "Jane Smith", "Mike Brown", "Emily Davis"]
    customers = ["Cust001", "Cust002", "Cust003"]
    
    data = {
        "ID": [i for i in range(1, rows + 1)],
        "Operator": [random.choice(operators) for _ in range(rows)],
        "Parent Order ID": [random.randint(1000, 2000) for _ in range(rows)],
        "Material Definition ID": [f"Part{random.randint(100, 999)}" for _ in range(rows)],
        "Status": [random.choice(statuses) for _ in range(rows)],
        "Location": [random.choice(locations) for _ in range(rows)],
        "QTY Required": [random.randint(50, 500) for _ in range(rows)],
        "QTY Complete": [random.randint(0, 500) for _ in range(rows)],
        "QTY Scrap": [random.randint(0, 50) for _ in range(rows)],
        "Due Date": [(datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d") for _ in range(rows)],
        "Start Date": [(datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d") for _ in range(rows)],
        "Complete Date": [(datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d") for _ in range(rows)],
        "Customer ID": [random.choice(customers) for _ in range(rows)]
    }
    return pd.DataFrame(data)

# Generate the data
work_orders_df = generate_work_orders(rows=1000)

# Save to a CSV file in the specified folder
file_path = r"C:\Users\pclay\OneDrive\Desktop\Business Files\work_orders_test.csv"
work_orders_df.to_csv(file_path, index=False)

print(f"File saved as {file_path}")

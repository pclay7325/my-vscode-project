import pandas as pd

# File path to the uploaded file (update this to your local file path)
file_path = "Machine,Runtime (minutes),Planned.xlsx"

try:
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Display the columns and a sample of the data
    print("Columns Detected:", data.columns.tolist())
    print("Sample Data:")
    print(data.head())
except Exception as e:
    print(f"An error occurred: {str(e)}")

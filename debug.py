import pandas as pd

file_path = r"C:\Users\EthanTran\OneDrive - Trial Behavior Consulting\Desktop\Automating The Question Verdicts\Recruit Spreadsheet_Guenther v. Hyundai.xlsx"

# First print all sheet names
xl = pd.ExcelFile(file_path)
print("Sheets:", xl.sheet_names)
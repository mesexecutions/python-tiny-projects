import pandas as pd
import os
from datetime import datetime
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from openpyxl.styles import NamedStyle

folder = r"C:\links\resources\bc_analysis"
csv_file = os.path.join(folder, "output_20250605_141830.csv")
excel_file = os.path.join(folder, "output_20250605_141830_fixed.xlsx")

# Read CSV
df = pd.read_csv(csv_file)

# Get the name of the second column (assumed to have the date string)
date_col = df.columns[1]

def parse_date(val):
    try:
        # Parse date with pandas, ignore errors
        dt = pd.to_datetime(val, errors='coerce', dayfirst=False)
        return dt
    except Exception:
        return pd.NaT

# Insert new column next to B with parsed dates
df.insert(2, "Corrected_Date", df[date_col].apply(parse_date))

# Create an openpyxl workbook and worksheet
wb = Workbook()
ws = wb.active

# Append headers
ws.append(df.columns.tolist())

# Append data rows
for row in dataframe_to_rows(df, index=False, header=False):
    ws.append(row)

# Column letter for Corrected_Date (3rd column = C)
corrected_date_col = 'C'

# Create a NamedStyle with MM/DD/YYYY format (string used directly)
date_style = NamedStyle(name="date_style", number_format="MM/DD/YYYY")

# Apply date style to all cells in Corrected_Date column except header
for cell in ws[corrected_date_col][1:]:
    cell.style = date_style

# Save the Excel workbook
wb.save(excel_file)

print(f"Saved fixed Excel file with MM/DD/YYYY date format at: {excel_file}")

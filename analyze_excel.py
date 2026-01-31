"""
Excel File Analyzer - Generate JSON output
"""

import pandas as pd
import json
from pathlib import Path

# Read the Excel file
excel_path = Path(__file__).parent / "assets" / "Cyber Resilience Maturity Assessment.xlsx"

# Load all sheets
xl_file = pd.ExcelFile(excel_path)

analysis = {
    "file_name": "Cyber Resilience Maturity Assessment.xlsx",
    "sheets": []
}

# Analyze each sheet
for sheet_name in xl_file.sheet_names:
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    sheet_info = {
        "name": sheet_name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "sample_data": df.head(20).fillna("").to_dict(orient='records')
    }
    
    analysis["sheets"].append(sheet_info)

# Save to JSON
output_path = Path(__file__).parent / "excel_analysis.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(analysis, f, indent=2, ensure_ascii=False)

print(f"Analysis saved to: {output_path}")
print(f"\nFound {len(analysis['sheets'])} sheets:")
for sheet in analysis["sheets"]:
    print(f"  - {sheet['name']}: {sheet['rows']} rows × {sheet['columns']} columns")

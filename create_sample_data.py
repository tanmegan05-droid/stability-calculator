"""
Module to create sample ship data Excel file for MV Del Monte
"""
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def create_sample_ship_data():
    """Create a sample Excel file with MV Del Monte ship particulars"""
    
    wb = Workbook()
    
    # Sheet 1: Ship Particulars
    ws_particulars = wb.active
    ws_particulars.title = "Ship Particulars"
    
    particulars_data = [
        ["Parameter", "Value", "Unit"],
        ["Ship Name", "MV Del Monte", ""],
        ["Length Overall (LOA)", "120.0", "m"],
        ["Length Between Perpendiculars (LBP)", "115.0", "m"],
        ["Breadth", "20.0", "m"],
        ["Depth", "10.0", "m"],
        ["Design Draft", "6.0", "m"],
        ["Lightship Weight", "2500", "tonnes"],
        ["Deadweight", "5000", "tonnes"],
    ]
    
    for row in particulars_data:
        ws_particulars.append(row)
    
    # Sheet 2: Displacement vs Draft
    ws_displacement = wb.create_sheet("Displacement Table")
    
    # Sample displacement data (Draft in meters, Displacement in tonnes)
    displacement_data = {
        "Draft (m)": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0],
        "Displacement (tonnes)": [2800, 3200, 3650, 4100, 4580, 5080, 5600, 6140, 6700, 7280, 7880, 8500, 9140],
    }
    
    df_displacement = pd.DataFrame(displacement_data)
    for row in dataframe_to_rows(df_displacement, index=False, header=True):
        ws_displacement.append(row)
    
    # Sheet 3: KN Curves (Cross Curves of Stability)
    ws_kn = wb.create_sheet("KN Curves")
    
    # KN values for different heel angles and displacements
    # Columns: Displacement (tonnes), then KN values at different heel angles
    kn_data = {
        "Displacement (tonnes)": [3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000],
        "KN at 10°": [0.45, 0.48, 0.51, 0.54, 0.57, 0.60, 0.63, 0.66, 0.69, 0.72, 0.75],
        "KN at 15°": [0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35],
        "KN at 20°": [1.25, 1.32, 1.39, 1.46, 1.53, 1.60, 1.67, 1.74, 1.81, 1.88, 1.95],
        "KN at 25°": [1.60, 1.69, 1.78, 1.87, 1.96, 2.05, 2.14, 2.23, 2.32, 2.41, 2.50],
        "KN at 30°": [1.90, 2.01, 2.12, 2.23, 2.34, 2.45, 2.56, 2.67, 2.78, 2.89, 3.00],
        "KN at 35°": [2.15, 2.28, 2.41, 2.54, 2.67, 2.80, 2.93, 3.06, 3.19, 3.32, 3.45],
        "KN at 40°": [2.35, 2.50, 2.65, 2.80, 2.95, 3.10, 3.25, 3.40, 3.55, 3.70, 3.85],
        "KN at 45°": [2.50, 2.67, 2.84, 3.01, 3.18, 3.35, 3.52, 3.69, 3.86, 4.03, 4.20],
        "KN at 50°": [2.60, 2.79, 2.98, 3.17, 3.36, 3.55, 3.74, 3.93, 4.12, 4.31, 4.50],
        "KN at 55°": [2.65, 2.86, 3.07, 3.28, 3.49, 3.70, 3.91, 4.12, 4.33, 4.54, 4.75],
        "KN at 60°": [2.68, 2.90, 3.12, 3.34, 3.56, 3.78, 4.00, 4.22, 4.44, 4.66, 4.88],
    }
    
    df_kn = pd.DataFrame(kn_data)
    for row in dataframe_to_rows(df_kn, index=False, header=True):
        ws_kn.append(row)
    
    # Save the workbook
    wb.save("data/MV_Del_Monte_Ship_Data.xlsx")
    print("Sample ship data Excel file created successfully!")

if __name__ == "__main__":
    create_sample_ship_data()

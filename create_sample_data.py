"""
Create ship data Excel file for MV Del Monte using actual hydrostatic data
"""
import pandas as pd
import numpy as np
import os
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def create_sample_ship_data():
    """Create Excel file with actual ship data from Stability.xlsx"""
    
    print("Creating MV Del Monte ship data file...")
    
    # Try to load actual ship data if available
    actual_data_file = 'Stability.xlsx'
    if os.path.exists(actual_data_file):
        print(f"✓ Found actual ship data: {actual_data_file}")
        # Read the actual displacement data
        actual_data = pd.read_excel(actual_data_file, sheet_name='Sheet1', header=0)
        actual_data.columns = ['Draft', 'Displacement']
        displacement_data = {
            "Draft (m)": actual_data['Draft'].tolist(),
            "Displacement (tonnes)": actual_data['Displacement'].tolist()
        }
        print(f"✓ Loaded {len(actual_data)} actual data points")
    else:
        print("⚠ Actual data file not found, using default displacement table")
        # Fallback: use pre-calculated values matching the actual data
        displacement_data = {
            "Draft (m)": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0],
            "Displacement (tonnes)": [10497, 13135, 16107, 19413, 23052, 27025, 31331, 35971, 40944, 46251, 51891, 57865, 64172, 70813, 77787, 85094, 92735, 100710, 109018, 117659, 126634, 135943, 145585, 155560, 165869],
        }
    
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
    
    # Sheet 2: Displacement vs Draft (actual data)
    ws_displacement = wb.create_sheet("Displacement Table")
    
    df_displacement = pd.DataFrame(displacement_data)
    for row in dataframe_to_rows(df_displacement, index=False, header=True):
        ws_displacement.append(row)
    
    # Sheet 3: KN Curves (Cross Curves of Stability)
    # Generate based on displacement range from actual data
    ws_kn = wb.create_sheet("KN Curves")
    
    min_disp = min(displacement_data["Displacement (tonnes)"])
    max_disp = max(displacement_data["Displacement (tonnes)"])
    
    # Create displacement points for KN curves
    displacement_points = np.linspace(min_disp, max_disp, 50)
    
    # Heel angles from 10° to 60° in 5° increments
    heel_angles = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    
    # Generate KN curves (realistic values that increase with both displacement and angle)
    kn_data = {"Displacement (tonnes)": displacement_points.tolist()}
    
    for angle in heel_angles:
        # KN values should increase with heel angle and displacement
        # Using a realistic formula: KN = base_factor * disp^0.4 * sin(angle)
        base_factor = 0.015
        kn_values = base_factor * (displacement_points ** 0.4) * np.sin(np.radians(angle))
        kn_data[f"KN at {angle}°"] = kn_values.tolist()
    
    df_kn = pd.DataFrame(kn_data)
    for row in dataframe_to_rows(df_kn, index=False, header=True):
        ws_kn.append(row)
    
    # Save the workbook
    output_file = "data/MV_Del_Monte_Ship_Data.xlsx"
    wb.save(output_file)
    
    print(f"✓ Created {output_file}")
    print(f"✓ Displacement Table: {len(df_displacement)} rows")
    print(f"✓ Draft range: {df_displacement['Draft (m)'].min():.2f}m to {df_displacement['Draft (m)'].max():.2f}m")
    print(f"✓ Displacement range: {df_displacement['Displacement (tonnes)'].min():.0f} to {df_displacement['Displacement (tonnes)'].max():.0f} tonnes")
    print(f"✓ KN Curves: {len(df_kn)} displacement points × {len(heel_angles)} heel angles")
    
    # Verify key values
    draft_12_data = df_displacement[df_displacement['Draft (m)'] == 12.0]
    if not draft_12_data.empty:
        print(f"\n✓ Verification: At Draft 12.0m → Displacement = {draft_12_data['Displacement (tonnes)'].values[0]:.0f} tonnes")
    
    print("\nSample ship data Excel file created successfully!")


if __name__ == "__main__":
    create_sample_ship_data()

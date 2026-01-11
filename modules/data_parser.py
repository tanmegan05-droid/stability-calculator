"""
Data parser module for reading ship data from Excel files
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional


class ShipDataParser:
    """Parse ship data from Excel file"""
    
    def __init__(self, excel_path: str):
        """Initialize parser with Excel file path"""
        self.excel_path = excel_path
        self.particulars = {}
        self.displacement_table = None
        self.kn_curves = None
        self._load_data()
    
    def _load_data(self):
        """Load all data from Excel file"""
        try:
            # Load ship particulars
            df_particulars = pd.read_excel(self.excel_path, sheet_name="Ship Particulars")
            for _, row in df_particulars.iterrows():
                param = row.get("Parameter", "")
                value = row.get("Value", "")
                if param and value:
                    self.particulars[param] = value
            
            # Load displacement table
            self.displacement_table = pd.read_excel(
                self.excel_path, sheet_name="Displacement Table"
            )
            
            # Load KN curves
            self.kn_curves = pd.read_excel(
                self.excel_path, sheet_name="KN Curves"
            )
            
        except Exception as e:
            raise ValueError(f"Error loading ship data: {str(e)}")
    
    def get_displacement_from_draft(self, draft: float) -> float:
        """
        Calculate displacement for given draft using linear interpolation
        
        Args:
            draft: Draft in meters
            
        Returns:
            Displacement in tonnes
        """
        if self.displacement_table is None:
            raise ValueError("Displacement table not loaded")
        
        drafts = self.displacement_table["Draft (m)"].values
        displacements = self.displacement_table["Displacement (tonnes)"].values
        
        # Check if draft is within range
        if draft < drafts.min() or draft > drafts.max():
            raise ValueError(
                f"Draft {draft}m is outside valid range "
                f"[{drafts.min()}, {drafts.max()}]m"
            )
        
        # Linear interpolation
        displacement = np.interp(draft, drafts, displacements)
        return float(displacement)
    
    def get_kn_value(self, displacement: float, heel_angle: float) -> float:
        """
        Get KN value for given displacement and heel angle using interpolation
        
        Args:
            displacement: Displacement in tonnes
            heel_angle: Heel angle in degrees
            
        Returns:
            KN value in meters
        """
        if self.kn_curves is None:
            raise ValueError("KN curves not loaded")
        
        # Get available heel angles from column names
        heel_columns = [col for col in self.kn_curves.columns if "KN at" in col]
        available_angles = [float(col.split("°")[0].split("at")[1].strip()) 
                           for col in heel_columns]
        
        # Check if heel angle is within range
        if heel_angle < min(available_angles) or heel_angle > max(available_angles):
            raise ValueError(
                f"Heel angle {heel_angle}° is outside valid range "
                f"[{min(available_angles)}, {max(available_angles)}]°"
            )
        
        displacements = self.kn_curves["Displacement (tonnes)"].values
        
        # Check if displacement is within range
        if displacement < displacements.min() or displacement > displacements.max():
            raise ValueError(
                f"Displacement {displacement}t is outside valid range "
                f"[{displacements.min()}, {displacements.max()}]t"
            )
        
        # Find the two closest heel angles
        sorted_angles = sorted(available_angles)
        angle_low = max([a for a in sorted_angles if a <= heel_angle])
        angle_high = min([a for a in sorted_angles if a >= heel_angle])
        
        # Get KN values for both angles
        col_low = f"KN at {int(angle_low)}°"
        col_high = f"KN at {int(angle_high)}°"
        
        kn_low = np.interp(displacement, displacements, self.kn_curves[col_low].values)
        kn_high = np.interp(displacement, displacements, self.kn_curves[col_high].values)
        
        # Interpolate between angles if necessary
        if angle_low == angle_high:
            return float(kn_low)
        else:
            kn_value = kn_low + (kn_high - kn_low) * (heel_angle - angle_low) / (angle_high - angle_low)
            return float(kn_value)
    
    def get_available_heel_angles(self) -> list:
        """Get list of available heel angles from KN curves"""
        if self.kn_curves is None:
            return []
        
        heel_columns = [col for col in self.kn_curves.columns if "KN at" in col]
        angles = [float(col.split("°")[0].split("at")[1].strip()) 
                 for col in heel_columns]
        return sorted(angles)
    
    def get_draft_range(self) -> Tuple[float, float]:
        """Get valid draft range"""
        if self.displacement_table is None:
            return (0.0, 0.0)
        
        drafts = self.displacement_table["Draft (m)"].values
        return (float(drafts.min()), float(drafts.max()))
    
    def get_ship_name(self) -> str:
        """Get ship name from particulars"""
        return self.particulars.get("Ship Name", "Unknown")

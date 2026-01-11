"""
Stability calculator module for computing GZ curves
"""
import numpy as np
from typing import Tuple, List
from modules.data_parser import ShipDataParser


# Constants for KG calculation
KG_BASE_FACTOR = 0.45  # Base KG as fraction of draft
KG_LOAD_ADJUSTMENT = 0.05  # Adjustment per 1000 tonnes of load


class StabilityCalculator:
    """Calculate stability parameters and GZ curves"""
    
    def __init__(self, ship_data_parser: ShipDataParser):
        """Initialize calculator with ship data parser"""
        self.parser = ship_data_parser
    
    def calculate_kg(self, load_kg: float, draft_m: float) -> float:
        """
        Calculate vertical center of gravity (KG)
        
        This is a simplified calculation. In reality, KG would depend on
        detailed loading conditions and compartment-wise cargo distribution.
        
        Args:
            load_kg: Load weight in kilograms
            draft_m: Draft in meters
            
        Returns:
            KG value in meters
        """
        # Simplified KG calculation based on draft
        # Typical KG is roughly 0.45-0.55 of the draft for cargo ships
        # Adding a small adjustment for load distribution
        # Assume cargo is loaded relatively low in the ship
        base_kg = KG_BASE_FACTOR * draft_m
        load_adjustment = (load_kg / 1000000) * KG_LOAD_ADJUSTMENT  # Adjustment per 1000 tonnes
        kg = base_kg + load_adjustment
        return kg
    
    def calculate_gz_with_kg(
        self, 
        draft_m: float, 
        kg: float, 
        heel_angles: List[float] = None
    ) -> Tuple[List[float], List[float], float]:
        """
        Calculate GZ values for different heel angles using provided KG
        
        GZ = KN - KG * sin(heel_angle)
        
        Args:
            draft_m: Draft in meters
            kg: Vertical center of gravity in meters
            heel_angles: List of heel angles in degrees (optional)
            
        Returns:
            Tuple of (heel_angles, gz_values, displacement)
        """
        # Get displacement from draft
        displacement = self.parser.get_displacement_from_draft(draft_m)
        
        # Use default heel angles if not provided
        if heel_angles is None:
            heel_angles = self.parser.get_available_heel_angles()
        
        gz_values = []
        
        for angle in heel_angles:
            # Get KN value from cross curves
            kn = self.parser.get_kn_value(displacement, angle)
            
            # Calculate GZ = KN - KG * sin(angle)
            angle_rad = np.radians(angle)
            gz = kn - kg * np.sin(angle_rad)
            gz_values.append(gz)
        
        return heel_angles, gz_values, displacement
    
    def calculate_gz(
        self, 
        draft_m: float, 
        load_kg: float, 
        heel_angles: List[float] = None
    ) -> Tuple[List[float], List[float], float, float]:
        """
        Calculate GZ values for different heel angles
        
        GZ = KN - KG * sin(heel_angle)
        
        Args:
            draft_m: Draft in meters
            load_kg: Load weight in kilograms
            heel_angles: List of heel angles in degrees (optional)
            
        Returns:
            Tuple of (heel_angles, gz_values, displacement, kg)
        """
        # Get displacement from draft
        displacement = self.parser.get_displacement_from_draft(draft_m)
        
        # Calculate KG
        kg = self.calculate_kg(load_kg, draft_m)
        
        # Use default heel angles if not provided
        if heel_angles is None:
            heel_angles = self.parser.get_available_heel_angles()
        
        gz_values = []
        
        for angle in heel_angles:
            # Get KN value from cross curves
            kn = self.parser.get_kn_value(displacement, angle)
            
            # Calculate GZ = KN - KG * sin(angle)
            angle_rad = np.radians(angle)
            gz = kn - kg * np.sin(angle_rad)
            gz_values.append(gz)
        
        return heel_angles, gz_values, displacement, kg
    
    def validate_input(self, draft_m: float, kg: float) -> Tuple[bool, str]:
        """
        Validate input parameters
        
        Args:
            draft_m: Draft in meters
            kg: Vertical center of gravity in meters
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check draft range
        min_draft, max_draft = self.parser.get_draft_range()
        
        if draft_m < min_draft:
            return False, f"Draft must be at least {min_draft} meters"
        
        if draft_m > max_draft:
            return False, f"Draft cannot exceed {max_draft} meters"
        
        # Check KG is positive
        if kg <= 0:
            return False, "KG (Vertical Center of Gravity) must be a positive value"
        
        # Check KG is reasonable (typically should be less than draft + depth)
        # For cargo ships, KG is typically between 0.4 * draft and 1.5 * draft
        if kg > max_draft * 2:
            return False, f"KG value seems unreasonably high (should typically be less than {max_draft * 2} meters)"
        
        return True, ""
    
    def convert_feet_to_meters(self, feet: float) -> float:
        """Convert feet to meters"""
        return feet * 0.3048
    
    def get_stability_summary(
        self, 
        heel_angles: List[float], 
        gz_values: List[float],
        displacement: float,
        kg: float
    ) -> dict:
        """
        Generate stability summary with key parameters
        
        Args:
            heel_angles: List of heel angles
            gz_values: List of GZ values
            displacement: Ship displacement
            kg: Vertical center of gravity
            
        Returns:
            Dictionary with stability summary
        """
        # Find maximum GZ and angle
        max_gz_idx = np.argmax(gz_values)
        max_gz = gz_values[max_gz_idx]
        max_gz_angle = heel_angles[max_gz_idx]
        
        # Find angle of vanishing stability (where GZ becomes negative)
        vanishing_angle = None
        for i, gz in enumerate(gz_values):
            if gz < 0:
                vanishing_angle = heel_angles[i]
                break
        
        # Calculate area under curve (righting energy) up to 30 degrees
        area_30 = 0
        for i in range(len(heel_angles) - 1):
            if heel_angles[i] <= 30 and heel_angles[i+1] <= 30:
                # Trapezoidal integration
                area_30 += (gz_values[i] + gz_values[i+1]) / 2 * (heel_angles[i+1] - heel_angles[i])
        
        summary = {
            "displacement_tonnes": round(displacement, 2),
            "kg_meters": round(kg, 3),
            "max_gz_meters": round(max_gz, 3),
            "max_gz_angle_degrees": round(max_gz_angle, 1),
            "area_under_curve_30deg": round(area_30, 3),
            "vanishing_angle_degrees": round(vanishing_angle, 1) if vanishing_angle else "N/A",
        }
        
        return summary

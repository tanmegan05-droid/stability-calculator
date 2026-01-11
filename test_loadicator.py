#!/usr/bin/env python3
"""
Test script for the Loadicator tool
Tests core functionality of data parsing, calculations, and plotting
"""

import sys
from modules.data_parser import ShipDataParser
from modules.stability_calculator import StabilityCalculator
from modules.plotter import StabilityPlotter

# Test constants
FEET_TO_METERS = 0.3048  # Conversion factor from feet to meters

def test_data_loading():
    """Test loading ship data from Excel"""
    print("Test 1: Loading ship data...")
    try:
        parser = ShipDataParser('data/MV_Del_Monte_Ship_Data.xlsx')
        ship_name = parser.get_ship_name()
        draft_range = parser.get_draft_range()
        print(f"  ✓ Ship name: {ship_name}")
        print(f"  ✓ Draft range: {draft_range[0]} - {draft_range[1]} m")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_displacement_calculation():
    """Test displacement calculation"""
    print("\nTest 2: Displacement calculation...")
    try:
        parser = ShipDataParser('data/MV_Del_Monte_Ship_Data.xlsx')
        draft = 5.5
        displacement = parser.get_displacement_from_draft(draft)
        print(f"  ✓ Draft {draft}m → Displacement {displacement}t")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_gz_calculation():
    """Test GZ calculation"""
    print("\nTest 3: GZ calculation...")
    try:
        parser = ShipDataParser('data/MV_Del_Monte_Ship_Data.xlsx')
        calculator = StabilityCalculator(parser)
        
        draft_m = 5.5
        load_kg = 500000
        
        heel_angles, gz_values, displacement, kg = calculator.calculate_gz(draft_m, load_kg)
        
        print(f"  ✓ Displacement: {displacement}t")
        print(f"  ✓ KG: {kg:.3f}m")
        print(f"  ✓ Number of GZ values: {len(gz_values)}")
        print(f"  ✓ Max GZ: {max(gz_values):.3f}m at {heel_angles[gz_values.index(max(gz_values))]}°")
        
        # Verify all GZ values are positive (ship is stable)
        if all(gz > 0 for gz in gz_values[:8]):  # Check first 8 angles
            print("  ✓ Ship shows positive stability")
        else:
            print("  ⚠ Warning: Some negative GZ values detected")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_input_validation():
    """Test input validation"""
    print("\nTest 4: Input validation...")
    try:
        parser = ShipDataParser('data/MV_Del_Monte_Ship_Data.xlsx')
        calculator = StabilityCalculator(parser)
        
        # Test valid input
        is_valid, msg = calculator.validate_input(5.5, 500000)
        if is_valid:
            print("  ✓ Valid input accepted")
        else:
            print(f"  ✗ Valid input rejected: {msg}")
            return False
        
        # Test invalid draft (too high)
        is_valid, msg = calculator.validate_input(10.0, 500000)
        if not is_valid:
            print(f"  ✓ Invalid draft rejected: {msg}")
        else:
            print("  ✗ Invalid draft accepted")
            return False
        
        # Test invalid load (negative)
        is_valid, msg = calculator.validate_input(5.5, -1000)
        if not is_valid:
            print(f"  ✓ Negative load rejected: {msg}")
        else:
            print("  ✗ Negative load accepted")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_plotting():
    """Test plot generation"""
    print("\nTest 5: Plot generation...")
    try:
        parser = ShipDataParser('data/MV_Del_Monte_Ship_Data.xlsx')
        calculator = StabilityCalculator(parser)
        plotter = StabilityPlotter()
        
        draft_m = 5.5
        load_kg = 500000
        
        heel_angles, gz_values, displacement, kg = calculator.calculate_gz(draft_m, load_kg)
        
        plot_path = plotter.plot_gz_curve(
            heel_angles,
            gz_values,
            parser.get_ship_name(),
            draft_m,
            displacement,
            'test_gz_curve.png'
        )
        
        print(f"  ✓ Plot generated: {plot_path}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_feet_conversion():
    """Test feet to meters conversion"""
    print("\nTest 6: Feet to meters conversion...")
    try:
        parser = ShipDataParser('data/MV_Del_Monte_Ship_Data.xlsx')
        calculator = StabilityCalculator(parser)
        
        feet = 18.0
        meters = calculator.convert_feet_to_meters(feet)
        expected = feet * FEET_TO_METERS
        
        if abs(meters - expected) < 0.001:
            print(f"  ✓ {feet} feet = {meters:.4f} meters")
            return True
        else:
            print(f"  ✗ Conversion error: expected {expected}, got {meters}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("LOADICATOR TEST SUITE")
    print("="*60)
    
    tests = [
        test_data_loading,
        test_displacement_calculation,
        test_gz_calculation,
        test_input_validation,
        test_plotting,
        test_feet_conversion,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("="*60)
    
    if all(results):
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

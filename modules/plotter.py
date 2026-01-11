"""
Plotting module for generating GZ stability curves
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web server
import matplotlib.pyplot as plt
import os
from typing import List


class StabilityPlotter:
    """Generate and save stability curve plots"""
    
    def __init__(self, output_dir: str = "modules/static/plots"):
        """Initialize plotter with output directory"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_gz_curve(
        self,
        heel_angles: List[float],
        gz_values: List[float],
        ship_name: str,
        draft: float,
        displacement: float,
        filename: str = "gz_curve.png"
    ) -> str:
        """
        Plot GZ stability curve
        
        Args:
            heel_angles: List of heel angles in degrees
            gz_values: List of GZ values in meters
            ship_name: Name of the ship
            draft: Draft in meters
            displacement: Displacement in tonnes
            filename: Output filename
            
        Returns:
            Path to saved plot file
        """
        plt.figure(figsize=(12, 8))
        
        # Plot GZ curve
        plt.plot(heel_angles, gz_values, 'b-', linewidth=2, label='GZ Curve')
        plt.plot(heel_angles, gz_values, 'bo', markersize=6)
        
        # Add zero line
        plt.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.5)
        
        # Mark maximum GZ
        max_idx = gz_values.index(max(gz_values))
        plt.plot(heel_angles[max_idx], gz_values[max_idx], 'ro', 
                markersize=10, label=f'Max GZ: {gz_values[max_idx]:.3f}m at {heel_angles[max_idx]:.1f}°')
        
        # Labels and title
        plt.xlabel('Heel Angle (degrees)', fontsize=12, fontweight='bold')
        plt.ylabel('GZ - Righting Lever (meters)', fontsize=12, fontweight='bold')
        plt.title(f'GZ Stability Curve - {ship_name}\n'
                 f'Draft: {draft:.2f}m | Displacement: {displacement:.2f} tonnes',
                 fontsize=14, fontweight='bold')
        
        # Grid
        plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        plt.grid(True, which='minor', alpha=0.1, linestyle='-', linewidth=0.3)
        plt.minorticks_on()
        
        # Legend
        plt.legend(loc='best', fontsize=10)
        
        # Tight layout
        plt.tight_layout()
        
        # Save plot
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def plot_comparison(
        self,
        heel_angles: List[float],
        gz_values_list: List[List[float]],
        labels: List[str],
        ship_name: str,
        filename: str = "gz_comparison.png"
    ) -> str:
        """
        Plot multiple GZ curves for comparison
        
        Args:
            heel_angles: List of heel angles in degrees
            gz_values_list: List of GZ value lists
            labels: List of labels for each curve
            ship_name: Name of the ship
            filename: Output filename
            
        Returns:
            Path to saved plot file
        """
        plt.figure(figsize=(12, 8))
        
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        
        # Plot each curve
        for i, (gz_values, label) in enumerate(zip(gz_values_list, labels)):
            color = colors[i % len(colors)]
            plt.plot(heel_angles, gz_values, color=color, linewidth=2, 
                    marker='o', markersize=4, label=label)
        
        # Add zero line
        plt.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.5)
        
        # Labels and title
        plt.xlabel('Heel Angle (degrees)', fontsize=12, fontweight='bold')
        plt.ylabel('GZ - Righting Lever (meters)', fontsize=12, fontweight='bold')
        plt.title(f'GZ Stability Curves Comparison - {ship_name}',
                 fontsize=14, fontweight='bold')
        
        # Grid
        plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        plt.minorticks_on()
        
        # Legend
        plt.legend(loc='best', fontsize=10)
        
        # Tight layout
        plt.tight_layout()
        
        # Save plot
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path

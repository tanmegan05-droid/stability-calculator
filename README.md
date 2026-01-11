# Loadicator - Ship Stability Calculator

A web-based ship stability calculator that computes and visualizes GZ (righting lever) curves for maritime vessels. Designed specifically for MV Del Monte but adaptable to any vessel through custom data upload.

## Features

- **Interactive Web Interface**: User-friendly Flask-based web application
- **Dynamic GZ Curve Generation**: Real-time computation and plotting of stability curves
- **Flexible Input**: Support for draft input in both meters and feet
- **Data Integration**: Parse Excel sheets containing ship particulars, displacement tables, and KN curves
- **Comprehensive Analysis**: 
  - Displacement calculation based on draft
  - KG (vertical center of gravity) estimation
  - GZ values computed for multiple heel angles
  - Stability parameters (max GZ, vanishing angle, area under curve)
- **Visual Output**: High-quality matplotlib plots with detailed stability information
- **Data Upload**: Capability to upload custom ship data via Excel files
- **Input Validation**: Comprehensive validation with clear error messages

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/tanmegan05-droid/stability-calculator.git
cd stability-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate sample ship data:
```bash
python create_sample_data.py
```

## Usage

### Starting the Application

Run the Flask application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Using the Calculator

1. **Navigate to the home page** - Enter draft and load values
2. **Select units** - Choose meters or feet for draft input
3. **Calculate** - Click "Calculate GZ Curve" to generate results
4. **View Results** - See the GZ curve plot and detailed stability parameters

### Uploading Custom Ship Data

1. Navigate to the **Upload Data** page
2. Prepare an Excel file with three sheets:
   - **Ship Particulars**: General ship information
   - **Displacement Table**: Draft vs Displacement data
   - **KN Curves**: Cross curves of stability
3. Upload the file and the system will validate and load the data

## Excel Data Format

### Sheet 1: Ship Particulars
| Parameter | Value | Unit |
|-----------|-------|------|
| Ship Name | MV Del Monte | |
| Length Overall (LOA) | 120.0 | m |
| Length Between Perpendiculars (LBP) | 115.0 | m |
| ... | ... | ... |

### Sheet 2: Displacement Table
| Draft (m) | Displacement (tonnes) |
|-----------|-----------------------|
| 2.0 | 2800 |
| 2.5 | 3200 |
| ... | ... |

### Sheet 3: KN Curves
| Displacement (tonnes) | KN at 10° | KN at 15° | KN at 20° | ... |
|----------------------|-----------|-----------|-----------|-----|
| 3000 | 0.15 | 0.28 | 0.42 | ... |
| 3500 | 0.16 | 0.30 | 0.45 | ... |
| ... | ... | ... | ... | ... |

## Technical Details

### Calculations

**GZ Formula:**
```
GZ = KN - KG × sin(heel_angle)
```

Where:
- **KN**: Cross curve value from ship's hydrostatic data
- **KG**: Vertical center of gravity (estimated from loading conditions)
- **heel_angle**: Angle of list in degrees

**Displacement:**
- Computed via linear interpolation from draft-displacement table

**KG Estimation:**
- Simplified calculation based on draft and load
- Formula: `KG = 0.55 × draft + (load_kg / 100000) × 0.1`

### Technology Stack

- **Backend**: Flask 3.0.0
- **Data Processing**: Pandas 2.1.4, NumPy 1.26.3
- **Visualization**: Matplotlib 3.8.2
- **Excel Parsing**: openpyxl 3.1.2

## Project Structure

```
stability-calculator/
├── app.py                      # Main Flask application
├── create_sample_data.py       # Script to generate sample Excel data
├── requirements.txt            # Python dependencies
├── app/
│   ├── data_parser.py         # Excel data parsing module
│   ├── stability_calculator.py # Stability computation module
│   ├── plotter.py             # Plotting module
│   ├── templates/             # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── results.html
│   │   ├── upload.html
│   │   └── about.html
│   └── static/
│       └── plots/             # Generated plot images
├── data/
│   └── MV_Del_Monte_Ship_Data.xlsx  # Sample ship data
└── uploads/                   # User-uploaded Excel files
```

## API Endpoints

- `GET /` - Home page with input form
- `POST /calculate` - Calculate stability and display results
- `GET /upload` - Upload page
- `POST /upload` - Process uploaded Excel file
- `GET /about` - Information about the tool

## Validation Rules

- Draft must be within the valid range defined in the displacement table
- Load must be positive and less than 10,000,000 kg (10,000 tonnes)
- Excel files must contain all required sheets with proper structure
- Heel angles and displacements must be within KN curve ranges

## Example Usage

**Input:**
- Draft: 5.5 meters
- Load: 500,000 kg (500 tonnes)

**Output:**
- Displacement: ~6,140 tonnes
- KG: ~3.525 meters
- Max GZ: Computed value at optimal heel angle
- GZ Curve: Visual plot showing stability at various heel angles

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available for maritime educational and professional use.

## References

- Ship Stability Theory and Practice
- IMO Intact Stability Code
- MV Del Monte Ship Particulars
- Cross Curves of Stability (KN Curves)

## Support

For issues or questions, please open an issue on the GitHub repository.

---

**Developed for maritime stability analysis and naval architecture applications**
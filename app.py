"""
Flask web application for the Loadicator Tool
"""
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
from modules.data_parser import ShipDataParser
from modules.stability_calculator import StabilityCalculator
from modules.plotter import StabilityPlotter

app = Flask(__name__, template_folder='modules/templates', static_folder='modules/static')
# Use environment variable for secret key, fallback to default for development
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'stability-calculator-secret-key-2026')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variable to store current ship data file
CURRENT_SHIP_DATA = 'data/MV_Del_Monte_Ship_Data.xlsx'


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}


@app.route('/')
def index():
    """Home page with input form"""
    try:
        # Load ship data to get available ranges
        parser = ShipDataParser(CURRENT_SHIP_DATA)
        draft_min, draft_max = parser.get_draft_range()
        ship_name = parser.get_ship_name()
        
        return render_template('index.html', 
                             draft_min=draft_min, 
                             draft_max=draft_max,
                             ship_name=ship_name)
    except Exception as e:
        flash(f'Error loading ship data: {str(e)}', 'error')
        return render_template('index.html', 
                             draft_min=0, 
                             draft_max=10,
                             ship_name="Unknown")


@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate stability and display results"""
    import traceback
    try:
        # Get form data
        draft_value = float(request.form.get('draft', 0))
        draft_unit = request.form.get('draft_unit', 'meters')
        load_kg = float(request.form.get('load', 0))
        
        # Convert draft to meters if needed
        if draft_unit == 'feet':
            calculator = StabilityCalculator(ShipDataParser(CURRENT_SHIP_DATA))
            draft_m = calculator.convert_feet_to_meters(draft_value)
        else:
            draft_m = draft_value
        
        # Load ship data and initialize calculator
        parser = ShipDataParser(CURRENT_SHIP_DATA)
        calculator = StabilityCalculator(parser)
        
        # Validate input
        is_valid, error_msg = calculator.validate_input(draft_m, load_kg)
        if not is_valid:
            flash(error_msg, 'error')
            return redirect(url_for('index'))
        
        # Calculate GZ curve
        heel_angles, gz_values, displacement, kg = calculator.calculate_gz(draft_m, load_kg)
        
        # Generate plot
        plotter = StabilityPlotter()
        plot_filename = f'gz_curve_{int(draft_m*100)}_{int(load_kg)}.png'
        plotter.plot_gz_curve(
            heel_angles, 
            gz_values, 
            parser.get_ship_name(),
            draft_m,
            displacement,
            plot_filename
        )
        
        # Get stability summary
        summary = calculator.get_stability_summary(heel_angles, gz_values, displacement, kg)
        
        # Prepare data for display
        curve_data = list(zip(heel_angles, [round(gz, 4) for gz in gz_values]))
        
        return render_template('results.html',
                             draft_input=draft_value,
                             draft_unit=draft_unit,
                             draft_m=round(draft_m, 3),
                             load_kg=load_kg,
                             load_tonnes=round(load_kg/1000, 2),
                             displacement=summary['displacement_tonnes'],
                             kg=summary['kg_meters'],
                             max_gz=summary['max_gz_meters'],
                             max_gz_angle=summary['max_gz_angle_degrees'],
                             area_30=summary['area_under_curve_30deg'],
                             vanishing_angle=summary['vanishing_angle_degrees'],
                             curve_data=curve_data,
                             plot_url=url_for('static', filename=f'plots/{plot_filename}'),
                             ship_name=parser.get_ship_name())
        
    except ValueError as e:
        flash(f'Input error: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        flash(f'Calculation error: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload new ship data Excel file"""
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Try to load and validate the file
            try:
                parser = ShipDataParser(filepath)
                # If successful, update the current ship data file
                global CURRENT_SHIP_DATA
                CURRENT_SHIP_DATA = filepath
                flash(f'Successfully loaded ship data for: {parser.get_ship_name()}', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error loading ship data from file: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload an Excel file (.xlsx or .xls)', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')


@app.route('/about')
def about():
    """About page with information about the tool"""
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

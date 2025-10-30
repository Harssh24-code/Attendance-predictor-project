import sys
import os
from flask import Flask, render_template, request, redirect, url_for

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from calc import calculate_stats, calculate_prediction 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    result = None

    if request.method == 'POST':
        try:
            
            attended_str = request.form.get('attended')
            total_str = request.form.get('total')
            target_str = request.form.get('target')

            
            attended = int(attended_str)
            total = int(total_str)
            target = int(target_str)

            if total <= 0 or target <= 0 or target > 100 or attended > total:
                error = "Please ensure Total Classes > 0, Target is between 1-100, and Attended ≤ Total."
                
                return render_template('index.html', error=error)

            
            stats = calculate_stats(attended, total, target)
            
            
            prediction = calculate_prediction(stats['current_pct'], attended, total, target) 

            
            result = {
                'current_pct': round(stats['current_pct'], 2),
                'target': target,
                'status': stats['status'],
                
                'action': prediction['action_needed'], 
            }

        except ValueError:
            
            error = "Invalid input. Please enter whole numbers for all fields."
        except Exception as e:
            
            if "action_needed" in str(e):
                 error = "A calculation key was missing. Please ensure input values are reasonable."
            else:
                
                error = f"An unexpected error occurred: {e}"

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)

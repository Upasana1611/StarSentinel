from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_script():
    script = request.form['script']
    result = ""

    try:
        if script == 'gnss':
            result = subprocess.run(['python', 'gnss_spoof_detector.py'], capture_output=True, text=True)
        elif script == 'satcom':
            result = subprocess.run(['python', 'satcom_scanner.py'], capture_output=True, text=True)
        elif script == 'space':
            result = subprocess.run(['python', 'space_traffic_sim.py'], capture_output=True, text=True)
        else:
            result = "Invalid selection"
        
        output = result.stdout if result.returncode == 0 else result.stderr
        
    except Exception as e:
        output = f"Error: {e}"

    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)

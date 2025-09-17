from flask import Flask, render_template_string
import subprocess
from threading import Timer
from typing import List
import os
from core.statements.html_template import html_template
from monitor.log_system import get_loggers

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()



def output_open_positions_to_browser(open_pos) -> None:
    """Output open positions for each account to HTML table"""
    
    app = Flask(__name__)
    
    # Create template context with abs function
    template_context = {
        'open_pos': open_pos,
        'abs': abs  # Make abs() available to template
    }
    
    @app.route('/')
    def show_positions():
        return render_template_string(
            html_template,  # First argument is the template string
            open_pos=open_pos,  # Then pass context variables as kwargs
            abs=abs  # Make abs() available to template
        )
    
    # Open browser after a short delay to ensure server is running
    Timer(1, open_browser).start()
    
    # Run the Flask app
    app.run(debug=False)
    
def open_browser():
    """Open browser considering WSL environment"""
    url = 'http://127.0.0.1:5000/'
    
    try:
        # Check if running in WSL
        if 'microsoft' in os.uname().release.lower():
            # Use cmd.exe to open default Windows browser
            subprocess.run(['cmd.exe', '/c', 'start', url], check=True)
        else:
            # Regular Linux browser handling
            browsers = ['firefox', 'google-chrome', 'chromium']
            for browser in browsers:
                if subprocess.run(['which', browser], capture_output=True).returncode == 0:
                    subprocess.Popen([browser, url])
                    return
            log_error.error("No suitable browser found")
    except Exception as e:
        log_error.error(f"Failed to open browser: {e}")


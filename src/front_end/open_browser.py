import subprocess
import os
from src.monitor.log_system import get_loggers

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()

    
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
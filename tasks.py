import subprocess
import sys
import os
import webbrowser

# --- Configuration ---
# The paths below assume you are running this script from the root /pytest directory.
# This variable points to the Python executable inside the currently active virtual environment (if activated).
PYTHON_EXECUTABLE = sys.executable 
REPORT_FILE = "report.html"


def run_tests():
    """Runs pytest and generates the HTML report (without opening)."""
    print("--- Running Pytest and Generating Report ---")
    
    # Construct the pytest command
    command = [
        PYTHON_EXECUTABLE,
        "-m", "pytest", 
        "-s", # Enables standard output (shows print statements from tests)
        f"--html={REPORT_FILE}", 
        "--self-contained-html"
    ]
    
    try:
        # check=False ensures the script doesn't crash if tests fail, 
        # allowing the report to still be generated.
        result = subprocess.run(command, check=False) 
        return result.returncode == 0
    except FileNotFoundError:
        print(f"Error: Python executable not found at {PYTHON_EXECUTABLE}")
        return False

def run_tests_and_open():
    """Runs tests, generates report, and opens the HTML file in the browser."""
    
    # 1. Execute the tests
    run_tests()
    
    # 2. Check if the report file was created
    report_path = os.path.abspath(REPORT_FILE)
    if os.path.exists(report_path):
        print(f"Report generated successfully at: {report_path}")
        # 3. Open the report in the default web browser
        webbrowser.open_new_tab(f"file://{report_path}")
        print("Opening report in default browser...")
    else:
        print("Error: HTML report file was not created. Check for test execution errors.")

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        # If no argument is provided, default to the 'report' command.
        run_tests_and_open()
        sys.exit(0)

    # Get the command and convert to lowercase as usual
    command = sys.argv[1].lower()

    if command == "test":
        run_tests()
    elif command == "report":
        run_tests_and_open()
    else:
        print(f"Unknown command: {command}. Use 'test' or 'report'.")
        print("Or run with no arguments for the default 'report' action.")

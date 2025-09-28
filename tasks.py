import subprocess
import sys
import os
import webbrowser

PYTHON_EXECUTABLE = sys.executable 
REPORT_FILE = "report.html"


def run_tests():
    """Runs pytest and generates the HTML report (without opening)."""
    print("--- Running Pytest and Generating Report ---")
    
    # Construct the pytest command
    command = [
        PYTHON_EXECUTABLE,
        "-m", "pytest", 
        "-s",
        f"--html={REPORT_FILE}", 
        "--self-contained-html"
    ]
    
    try:
        # check=False ensures the script doesn't crash if tests fail, allowing the report to still be generated.
        result = subprocess.run(command, check=False) 
        return result.returncode == 0
    except FileNotFoundError:
        print(f"Error: Python executable not found at {PYTHON_EXECUTABLE}")
        return False

def run_tests_and_open():
    """Runs tests, generates report, and attempts to open the HTML file in the browser based on OS."""
    
    # 1. Execute the tests
    run_tests()
    
    # 2. Check if the report file was created
    report_path = os.path.abspath(REPORT_FILE)
    if os.path.exists(report_path):
        print("\n" + "="*50)
        print("✅ Report generated successfully!")
        print(f"File Path: {report_path}")
        print("="*50)
        
        # 3. Attempt to open the report based on the operating system
        try:
            if sys.platform.startswith('win'):
                # Use webbrowser for native Windows environments
                webbrowser.open_new_tab(f"file://{report_path}")
                print("Attempting to open report using Windows default browser...")
            elif sys.platform.startswith('darwin'):
                # Use webbrowser for macOS
                webbrowser.open_new_tab(f"file://{report_path}")
                print("Attempting to open report using macOS default browser...")
            elif sys.platform.startswith('linux'):
                # For Linux and WSL, use the 'xdg-open' command (standard for Linux desktops) or 'wslview' (better for WSL, if available), falling back to just printing the path.
                try:
                    # Try wslview first for WSL environments
                    subprocess.run(['wslview', report_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print("Attempting to open report using 'wslview'...")
                except (FileNotFoundError, subprocess.CalledProcessError):
                    # Fallback to xdg-open for non-WSL Linux or if wslview is missing
                    try:
                        subprocess.run(['xdg-open', report_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print("Attempting to open report using 'xdg-open'...")
                    except (FileNotFoundError, subprocess.CalledProcessError):
                        print("\n>> Automatic open failed (wslview/xdg-open not found or working).")
                        print(">> Please copy the file path and paste it into your browser manually.")
            else:
                print("\n>> Automatic open failed for unknown OS.")
                print(">> Please copy the file path and paste it into your browser manually.")
                
        except Exception as e:
            print(f"Warning: Failed to automatically open browser. Error: {e}")
            print(">> Please copy the file path and paste it into your browser manually.")

    else:
        print("Error: HTML report file was not created. Check for test execution errors.")

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        # If no argument is provided, default to the 'report' command.
        run_tests_and_open()
        sys.exit(0)

    # Get the command and convert to lowercase
    command = sys.argv[1].lower()

    if command == "test":
        run_tests()
    elif command == "report":
        run_tests_and_open()
    else:
        print(f"Unknown command: {command}. Use 'test' or 'report'.")
        print("Or run with no arguments for the default 'report' action.")

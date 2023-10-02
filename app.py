import threading
import subprocess
import os

CURRENT_DIRECTORY = os.getcwd()

def run_script(script_name):
    global CURRENT_DIRECTORY

    # Use subprocess to run the script as a separate process
    subprocess.run([fr"{CURRENT_DIRECTORY}\.venv\Scripts\python.exe", fr"{CURRENT_DIRECTORY}\smartpark\{script_name}"])


if __name__ == "__main__":
    # Create a thread for each script
    sensor_thread = threading.Thread(target=run_script, args=("sensor.py",), daemon=False)
    carpark_thread = threading.Thread(target=run_script, args=("carpark.py",), daemon=True)  # Daemon Thread for carpark
    display_thread = threading.Thread(target=run_script, args=("display.py",), daemon=False)

    # Start all threads
    sensor_thread.start()
    carpark_thread.start()
    display_thread.start()

    # Wait for all threads to finish
    # No need to close daemon thread
    sensor_thread.join()
    display_thread.join()

    print("Closing Car Park Simulation Program")

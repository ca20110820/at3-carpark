import threading
import subprocess
import os

CURRENT_DIRECTORY = os.getcwd()

def run_script(script_name):
    global CURRENT_DIRECTORY

    # Use subprocess to run the script as a separate process
    subprocess.run([fr"{CURRENT_DIRECTORY}\.venv\Scripts\python.exe", fr"{CURRENT_DIRECTORY}\smartpark\{script_name}"])

print(CURRENT_DIRECTORY)

if __name__ == "__main__":
    # Create a thread for each script
    thread1 = threading.Thread(target=run_script, args=("sensor.py",), daemon=False)
    thread2 = threading.Thread(target=run_script, args=("carpark.py",), daemon=True)
    thread3 = threading.Thread(target=run_script, args=("display.py",), daemon=False)

    # Start all threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

    print("All scripts have finished.")

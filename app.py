import concurrent.futures
import subprocess
import os


def run_script(script_name):
    cwd = os.getcwd()

    # Use subprocess to run the script as a separate process
    subprocess.run([fr"{cwd}\.venv\Scripts\python.exe", fr"{cwd}\smartpark\{script_name}"])


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(run_script, "sensor.py")
        executor.submit(run_script, "carpark.py")
        executor.submit(run_script, "display.py")

    print("Closing Car Park Simulation Program")

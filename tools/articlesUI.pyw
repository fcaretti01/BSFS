import subprocess
import os
import sys

# Define the path to the Python script
script_path = os.path.join(os.path.dirname(__file__), r"latest_papers\articlesUI.pyw")  # Adjust this path as needed

# Run the Python script
result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

# Print the output and error (if any)
print(result.stdout)
if result.stderr:
    print(f"Error: {result.stderr}")

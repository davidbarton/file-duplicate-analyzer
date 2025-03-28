import sys
import subprocess

from src.lib.config import Config
from src.lib.file_operations import create_dir, write_text_data

def export_directory_structure(*, backend_name):
  """Export directory structure using rclone."""
  # Export directory structure
  result = subprocess.run(
    ["rclone", "lsjson", "--recursive", f"{backend_name}:"],
    capture_output=True,
    text=True
  )

  if result.returncode != 0:
    print(f"Error: Exporting directory structure: {result.stderr}.")
    sys.exit(1)

  return result.stdout

def main():
  """Export directory structure."""
  # Load variables from config
  backend_name = Config.get('backend_name')
  output_dir = Config.get('output_dir')
  script_name = Config.get('export_name')

  # Create output directory
  create_dir(dirpath=output_dir)

  # Define file paths
  output_file = f"{output_dir}/{backend_name}.{script_name}.json"

  # Do the thing
  output_data = export_directory_structure(backend_name=backend_name)
  count = len(output_data) - 2

  # Write output
  write_text_data(filepath=output_file, data=output_data)
  print(f"[0] {backend_name} directory structure has been saved to {output_file} with {count} entries.")

import os
import sys
import json
import yaml

def create_dir(*, dirpath):
  """Create directory if it doesn't exist."""
  os.makedirs(dirpath, exist_ok=True)

def check_file_exists(*, filepath):
  """Check if file exists."""
  if not os.path.exists(filepath):
    print(f"Error: File at path {filepath} not found.")
    sys.exit(1)

def read_json_file(*, filepath):
  """Read JSON file from backend."""
  check_file_exists(filepath=filepath)
  with open(filepath, 'r') as f:
    data = json.load(f)
  return data

def write_text_data(*, filepath, data, accessor=None):
  """Write filtered data to a file."""
  accessor = accessor or (lambda item: item)
  with open(filepath, 'w', encoding='utf-8') as f:
    if isinstance(data, (list, tuple, set)):
      for item in data:
        f.write(f"{accessor(item)}\n")
    else:
      f.write(data)

def read_yaml_file(*, filepath):
  """Read YAML file from backend."""
  check_file_exists(filepath=filepath)
  with open(filepath, 'r') as f:
    return yaml.safe_load(f)

import unicodedata

from src.lib.config import Config
from src.lib.file_operations import read_json_file, write_text_data

def find_dirs(*, data, whitelist):
  """Organize data into directories."""

  filtered = []
  for item in data:
    # Skip non-directories
    if not item['IsDir']:
      continue

    # Normalize paths
    dirname = unicodedata.normalize('NFC', item['Name'])

    # Find whitelist directories
    if any(dirname == whitelisted for whitelisted in whitelist):
      filtered.append(item)

  return filtered


def main():
  """Find directories in the backend."""
  # Load variables from config
  backend_name = Config.get('backend_name')
  output_dir = Config.get('output_dir')
  input_name = Config.get('export_name')
  script_name = Config.get('find_dirs_name')
  find_dirs_whitelist = Config.get('find_dirs_whitelist', [])

  # Define file paths
  input_file = f"{output_dir}/{backend_name}.{input_name}.json"
  output_file = f"{output_dir}/{backend_name}.{script_name}.txt"

  # Do the thing
  input_data = read_json_file(filepath=input_file)
  output_data = find_dirs(data=input_data, whitelist=find_dirs_whitelist)

  # Write output
  write_text_data(filepath=output_file, data=output_data, accessor=lambda item: item['Path'])
  print(f"[1] Wrote {len(output_data)} found directories to {output_file}.")

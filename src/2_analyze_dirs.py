from pathlib import Path
from collections import defaultdict

from src.lib.config import Config
from src.lib.file_operations import read_json_file, write_text_data
from src.lib.disk_objects import normalize_disk_object, format_output

def analyze_data(*, data, ignore_levels, ignore_dirs_blacklist):
  """Organize data into directories."""

  # Preprocess data
  index = 0
  total_size = 0
  to_evaluate = []
  dirs = defaultdict(lambda: {"Files": [], "Size": 0, "FileCount": 0})
  for item in data:
    index += 1
    item = normalize_disk_object(item=item, index=index, ignored_names=ignore_dirs_blacklist)

    # Filter out ignored paths
    if not item:
      continue

    total_size += item['Size']

    # Group files by their directory
    if item['IsDir']:
      if item['Level'] > ignore_levels:
        # Create a directory entry with all item properties except Size
        dir_entry = {k: v for k, v in item.items() if k != 'Size'}
        # Initialize the directory with proper structure if it doesn't exist
        dirs[item['DirPath']] = {**dirs[item['DirPath']], **dir_entry}
      if item['Level'] > ignore_levels + 1:
        # Add to evaluation list if it's not the top level directory
        to_evaluate.append(item['DirPath'])
    else:
      if item['Level'] > ignore_levels + 1:
        # Add file to directory stats
        dirs[item['DirPath']]['Files'].append(item)
        dirs[item['DirPath']]['Size'] += item['Size']
        dirs[item['DirPath']]['FileCount'] += 1

  # Evaluate parent directories
  for dir_path in to_evaluate:
    parent = str(Path(dirs[dir_path]['DirPath']).parent)
    dirs[parent]['Files'].extend(dirs[dir_path]['Files'])
    dirs[parent]['Size'] += dirs[dir_path]['Size']
    dirs[parent]['FileCount'] += dirs[dir_path]['FileCount']
    if dirs[parent]['Level'] > ignore_levels + 1:
      to_evaluate.append(parent)

  by_size = dict()
  for item in dirs.values():
    by_size[item['Size']] = {
      **by_size.get(item['Size'], dict()),
      'Size': item['Size'],
      'Items': by_size.get(item['Size'], dict()).get('Items', []) + [item]
    }

  sorted_by_size = sorted(by_size.values(), key=lambda item: item['Size'], reverse=True)

  def is_match(items):
    if len(items) < 2:
      return False
    for item1 in items:
      for item2 in items:
        if not (Path(item1['Path']).is_relative_to(item2['Path'])) and not (Path(item2['Path']).is_relative_to(item1['Path'])):
          return True
    return False

  summary = []
  result = []
  for size_group in sorted_by_size:
    size_group['Items'].sort(key=lambda x: x['Path'])
    if is_match(size_group['Items']):
      for item in size_group['Items']:
        item['Match'] = '[x]'
      summary.append(size_group['Items'])
    result.extend(size_group['Items'])

  return total_size, summary, result

def main():
  # Load variables from config
  backend_name = Config.get('backend_name')
  output_dir = Config.get('output_dir')
  input_name = Config.get('export_name')
  script_name = Config.get('analyze_dirs_name')
  ignore_levels = Config.get('ignore_levels')
  ignore_dirs_blacklist = Config.get('ignore_dirs_blacklist', [])

  # Define file paths
  input_file = f"{output_dir}/{backend_name}.{input_name}.json"
  output_file = f"{output_dir}/{backend_name}.{script_name}.txt"

  # Do the thing
  input_data = read_json_file(filepath=input_file)
  total_size, summary, result = analyze_data(data=input_data, ignore_levels=ignore_levels, ignore_dirs_blacklist=ignore_dirs_blacklist)
  output_data = format_output(total_size=total_size, summary=summary, result=result, isDir=True)
  write_text_data(filepath=output_file, data=output_data)
  print(f"[2] Directory analysis results written to: {output_file}.")

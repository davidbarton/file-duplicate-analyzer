from src.lib.config import Config
from src.lib.file_operations import read_json_file, write_text_data
from src.lib.disk_objects import normalize_disk_object, format_output

def analyze_data(*, data, ignore_dirs_blacklist, ignore_files_blacklist):
  """Analyze JSON file for duplicate files (same name and size, different paths)."""
  index = 0
  total_size = 0
  by_size = dict()
  for item in data:
    index += 1
    item = normalize_disk_object(item=item, index=index, ignored_names=ignore_dirs_blacklist)
    if item and not item['IsDir']:
      total_size += item['Size']
      by_size[item['Size']] = {
        **by_size.get(item['Size'], dict()),
        'Size': item['Size'],
        'Items': by_size.get(item['Size'], dict()).get('Items', []) + [item]
      }

  sorted_by_size = sorted(by_size.values(), key=lambda item: item['Size'], reverse=True)

  def is_match(items):
    if len(items) < 2:
      return False
    if any([item['Path'] in ignore_files_blacklist for item in items]):
      return False
    return True

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
  script_name = Config.get('analyze_files_name')
  ignore_dirs_blacklist = Config.get('ignore_dirs_blacklist', [])
  ignore_files_blacklist = Config.get('ignore_files_blacklist', [])

  # Define file paths
  input_file = f"{output_dir}/{backend_name}.{input_name}.json"
  output_file = f"{output_dir}/{backend_name}.{script_name}.txt"

  # Do the thing
  input_data = read_json_file(filepath=input_file)
  total_size, summary, result = analyze_data(data=input_data, ignore_dirs_blacklist=ignore_dirs_blacklist, ignore_files_blacklist=ignore_files_blacklist)
  output_data = format_output(total_size=total_size, summary=summary, result=result, isDir=False)
  write_text_data(filepath=output_file, data=output_data)
  print(f"[3] File analysis results written to: {output_file}.")

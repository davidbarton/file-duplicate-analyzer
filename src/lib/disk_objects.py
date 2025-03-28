import sys

import unicodedata
from pathlib import Path

def normalize_disk_object(*, item, index, ignored_names=None):
  """Normalize paths in the data."""
  item['Index'] = index
  item['Match'] = None
  item['Level'] = len(Path(item['Path']).parts)
  item['Name'] = unicodedata.normalize('NFC', item['Name'])
  item['Path'] = unicodedata.normalize('NFC', item['Path'])

  if item['IsDir']:
    item['DirPath'] = item['Path']
  else:
    item['DirPath'] = str(Path(item['Path']).parent)

  if any(ignored in Path(item['Path']).parts for ignored in ignored_names or []):
    return None

  return item

def format_size(size_in_bytes):
  """Format size in bytes to a human-readable format."""
  # Convert string to int if needed
  if isinstance(size_in_bytes, str):
    try:
      size_in_bytes = int(size_in_bytes)
    except ValueError:
      return "0 B"

  if size_in_bytes < 0:
    return "0 B"

  # Handle bytes
  if size_in_bytes < 1024:
    return f"{size_in_bytes} B"

  # Handle kilobytes
  size_in_kb = size_in_bytes / 1024
  if size_in_kb < 1024:
    if size_in_kb < 10:
      return f"{size_in_kb:.2f} KB"
    elif size_in_kb < 100:
      return f"{size_in_kb:.1f} KB"
    else:
      return f"{size_in_kb:.0f} KB"

  # Handle megabytes
  size_in_mb = size_in_kb / 1024
  if size_in_mb < 1024:
    if size_in_mb < 10:
      return f"{size_in_mb:.2f} MB"
    elif size_in_mb < 100:
      return f"{size_in_mb:.1f} MB"
    else:
      return f"{size_in_mb:.0f} MB"

  # Handle gigabytes and larger
  size_in_gb = size_in_mb / 1024
  if size_in_gb < 10:
    return f"{size_in_gb:.2f} GB"
  elif size_in_gb < 100:
    return f"{size_in_gb:.1f} GB"
  else:
    return f"{size_in_gb:.0f} GB"

def format_output(*, total_size, summary, result, isDir):
  def get_value(item, key, *, default=None):
    return item.get(key) or default or ''

  def format_line(*, item, title=None, msg=None):
    if not item:
      if not title:
        print("Error: Title is required.")
        sys.exit(1)
      formatted_msg = f" - {msg}" if msg else ''
      if isDir:
        return f"{title:<10} {'[Size]':>6} {'[FileCount]':>11} {'[Match]'} {'[Path]'}{formatted_msg}"
      else:
        return f"{title:<10} {'[Size]':>6} {'[Match]'} {'[Path]'}{formatted_msg}"
    if isDir:
      return f"{format_size(get_value(item, 'Size', default='0')):>17} {get_value(item, 'FileCount', default='0'):>11} {get_value(item, 'Match'):>7} {get_value(item, 'Path')}"
    else:
      return f"{format_size(get_value(item, 'Size', default='0')):>17} {get_value(item, 'Match'):>7} {get_value(item, 'Path')}"

  msg_duplicate_size = None
  if not isDir:
    match_file_size = 0
    for group in summary:
      match_file_size += group[0]['Size'] * (len(group) - 1)
    msg_duplicate_size = f" You can save {format_size(match_file_size)} by removing duplicates."

  summary_count = [len(group) for group in summary]
  summary_msg = f"Found {sum(summary_count)} matches across {len(summary)} groups.{msg_duplicate_size or ''}" if len(summary) > 0 else None

  summary_lines = [format_line(item=None, title="MATCHES", msg=summary_msg)]
  result_lines = ["", format_line(item=None, title="ALL", msg=f"Analyzed {len(result)} files with total size of {format_size(total_size)}.")]

  if len(summary) > 0:
    for group in summary:
      summary_lines.append("")
      for item in group:
        summary_lines.append(format_line(item=item))
  else:
    summary_lines.extend(["", "    No matches found."])

  for item in result:
    result_lines.append(format_line(item=item))

  return summary_lines + result_lines

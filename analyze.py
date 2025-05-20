import sys
from importlib import import_module

from src.lib.config import Config

def main():
  if len(sys.argv) > 1:
    print(f"Using config file: {sys.argv[1]}")
    Config.init(config_file=sys.argv[1])
  execute_scripts = Config.get("execute_scripts", "all")

  scripts = [
    import_module("src.0_export"),
    import_module("src.1_find_dirs"),
    import_module("src.2_analyze_dirs"),
    import_module("src.3_analyze_files")
  ]

  for index, script in enumerate(scripts):
    if execute_scripts == "all" or index is int(execute_scripts):
      script.main()

if __name__ == "__main__":
  main()

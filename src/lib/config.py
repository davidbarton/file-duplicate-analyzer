import sys

from .file_operations import read_yaml_file

DEFAULT_CONFIG_FILE = "config.yaml"
DEFAULT_REQUIRED_VALUES = [
  "backend_name",
  "output_dir",
  "export_name",
  "find_dirs_name",
  "analyze_dirs_name",
  "analyze_files_name",
  "ignore_levels",
  "find_dirs_whitelist",
  "ignore_dirs_blacklist",
  "ignore_files_blacklist",
]
DEFAULT_VALUES = dict(
  output_dir="output",
  export_name="0_export",
  find_dirs_name="1_find_dirs",
  analyze_dirs_name="2_analyze_dirs",
  analyze_files_name="3_analyze_files"
)

class Config:
  """Singleton for config values."""
  _instance = None
  _config_values = None
  _required_values = None
  _initialized = False

  @classmethod
  def init(cls, *, config_file=None, required_values=None):
    """Initialize Config singleton manually. Can be called only once."""
    if cls._instance:
      print("Error: Config already initialized.")
      sys.exit(1)
    else:
      cls._instance = cls.__new__(cls)
      cls._instance._init(config_file=config_file or DEFAULT_CONFIG_FILE, required_values=required_values or DEFAULT_REQUIRED_VALUES)

    return cls._instance

  @classmethod
  def get(cls, key, default=None):
    """Get config value."""
    parts = key.split('.')
    value = cls._get_instance()._config_values
    for part in parts:
      value = value.get(part, default)
    return value

  @classmethod
  def _get_instance(cls):
    """Get singleton instance."""
    if cls._instance is None:
      cls.init()
    return cls._instance

  def __init__(self, *args, **kwargs):
    """Prevent direct instantiation."""
    raise RuntimeError("Use Config.init() instead")

  def _init(self, *, config_file, required_values):
    """Internal initialization method."""
    if not self._initialized:
      self._config_file = config_file
      self._required_values = required_values
      self._load_config_values()
      self._ensure_required_values()
      self._initialized = True

  def _load_config_values(self):
    """Read config values from config file."""
    self._config_values = {**DEFAULT_VALUES, **read_yaml_file(filepath=self._config_file)}

  def _ensure_required_values(self):
    """Ensure required config values are set."""
    for key in self._required_values:
      if key not in self._config_values or self._config_values[key] is None or self._config_values[key] == "":
        print(f"Error: Please provide {key} value.")
        sys.exit(1)

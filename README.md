# 🗃️ File Duplicate Analyzer

Finds duplicate files on your filesystem.

## How to use

1. Create an rclone backend, see [https://rclone.org/commands/rclone_config](https://rclone.org/commands/rclone_config)
2. Edit config in `config.yaml` file
3. Run `python analyze.py`
4. Inspect output files in `output` directory
5. Remove duplicates from your filesystem
6. Go back to step 2 and repeat the process until satisfied

## Using alternate config

- You can also create alternate configs like `dummy.config.yaml`
- And run script with `python analyze.py dummy.config.yaml`

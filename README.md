# Retroarch Save Sync
<p align="center"> <img width="256" height="256"  src="https://github.com/user-attachments/assets/43872c31-1975-4e55-b05e-712f2b50fe8c" /> </p>


A Python script to synchronize RetroArch game saves between a Mac (or python 3 supported environment) and a retro handheld device.


It ensures both devices have the latest save files by comparing file contents, backing up existing saves with timestamped archives, and optionally syncing game states.

This is useful if your device doesnt permit the use of Wifi / Cloud saves / Syncthing like Ambernic RG35xx (OG), RG28xx, Miyoo Mini..

## Features

- Bidirectional sync of RetroArch saves based on file content, size, and existence.
- Ignores hidden files (dotfiles) like `.DS_Store`.
- Optional timestamped backups with retention of the 5 most recent backups.
- Supports syncing the "states" folder located alongside the saves folder.
- Dry run mode to preview changes without copying files.
- Safe copying with fallback for metadata issues on non-native filesystems.
- Progress bar and detailed status messages during sync and backup.
- Configurable via command-line arguments.

## Installation

1. Make sure Python 3 is installed on your Mac.
2. Install required package:

pip3 install tqdm

3. Download or clone this repository.
4. Place the `sync_retroarch.py` script in a convenient folder.

## Usage

Run the script from the terminal with:

python3 Retroarch_Save_Sync.py -mp /path/to/local/saves -hp /path/to/handheld/saves [options]


### Options

- `--backup` : Enable backup of saves before syncing.
- `--dryrun` : Show what would be copied/backed up without changes.
- `--transfer-states` : Also sync the "states" folder alongside saves. 
- `-mb PATH` : Custom backup folder on local. (Optional, default in saves folder)
- `-hb PATH` : Custom backup folder on handheld. (Optional, default in saves folder)
- `-msb PATH` : Custom backup folder for states on local. (Optional, default in states folder)
- `-hsb PATH` : Custom backup folder for states on handheld. (Optional, default in states folder)


### Example

python3 Retroarch_Save_Sync.py -mp ~/RetroArch/saves -hp /Volumes/Handheld/RetroArch/saves --backup --transfer-states


## Notes

- Ensure paths are accessible and writable.
- Backups are stored with timestamped zip files, older backups are pruned automatically.
- The script uses file hashing to detect real changes, avoiding redundant copies.
- Supports external and network drives with metadata-safe copying.

## License

This project is licensed under the MIT License.

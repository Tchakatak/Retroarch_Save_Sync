# Retroarch Save Sync
<p align="center"> <img width="256" height="256"  src="https://github.com/user-attachments/assets/43872c31-1975-4e55-b05e-712f2b50fe8c" /> </p>


A Python script to synchronize RetroArch game saves between a unix machine and a retro handheld device running retroarch (or any CFW based on retroarch).


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

1. Make sure Python 3 is installed on your local.
2. Install required package:
```  
pip3 install tqdm
```
3. Download or clone this repository.
4. Place the `Retroarch_Save_Sync.py` script in a convenient folder.

## Usage

Run the script from the terminal with:
```
python3 Retroarch_Save_Sync.py -lp /path/to/local/saves -hp /path/to/handheld/saves [options]
```
### Options

| Option                          | Description                                                     | Default / Required                         |
|---------------------------------|-----------------------------------------------------------------|--------------------------------------------|
| `-lp`, `--localpath`            | Path to RetroArch saves folder on local                         | **Required**                               |
| `-hp`, `--handheldpath`         | Path to RetroArch saves folder on handheld                      | **Required**                               |
| `--backup`                      | Enable backup of saves and states before syncing                | Optional                                   |
| `--dryrun`                      | Show planned actions without making changes                     | Optional                                   |
| `--transfer-states`             | Also sync the states folder located alongside the saves folder  | Optional                                   |
| `-lb`, `--localbackup`          | Custom backup folder on local                                   | `<localpath>/backups`                      |
| `-hb`, `--handheldbackup`       | Custom backup folder on handheld                                | `<handheldpath>/backups`                   |
| `-lsb`, `--localstatesbackup`   | Custom backup folder for local states                           | `<local_states>/backups` (if applicable)   |
| `-hsb`, `--handheldstatesbackup`| Custom backup folder for handheld states                        | `<handheld_states>/backups` (if applicable)|
| `--localstate`                  | Custom states folder path on local (overrides auto-detect)      | Auto-detected from saves folder parent     |
| `--handheldstate`               | Custom states folder path on handheld (overrides auto-detect)   | Auto-detected from saves folder parent     |


### Example
```
python3 Retroarch_Save_Sync.py -lp ~/RetroArch/saves -hp /Volumes/Handheld/RetroArch/saves --backup --transfer-states
```
## Notes

- Ensure paths are accessible and writable.
- Backups are stored with timestamped zip files, older backups are pruned automatically.
- The script uses file hashing to detect real changes, avoiding redundant copies.
- Supports external and network drives with metadata-safe copying.


## License

This project is licensed under the MIT License.

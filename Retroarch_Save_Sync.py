import os
import shutil
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import argparse

def should_ignore(filepath):
    # Ignore all hidden files and folders (starting with dot)
    for part in filepath.parts:
        if part.startswith('.'):
            return True
    return False

def clean_backups_folder(backup_dir, keep=5):
    backup_dir = Path(backup_dir)
    if not backup_dir.is_dir():
        return
    backups = sorted(
        [f for f in backup_dir.iterdir() if f.is_file() and f.suffix == '.zip'],
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    for old_backup in backups[keep:]:
        print(f"Removing old backup: {old_backup}")
        old_backup.unlink()

def backup_saves(saves_dir, backup_dir, dryrun=False):
    print(f"Backing up saves in {saves_dir}...")
    backup_dir = Path(backup_dir)
    if dryrun:
        print(f"[Dry Run] Would create backup directory: {backup_dir}")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_file = backup_dir / f"saves_backup_{timestamp}.zip"
        print(f"[Dry Run] Would create backup zip file: {backup_file}")
        files = [f for f in Path(saves_dir).rglob("*") 
                 if f.is_file() and not should_ignore(f.relative_to(saves_dir))]
        print(f"[Dry Run] Would zip {len(files)} files.")
        return

    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = backup_dir / f"saves_backup_{timestamp}.zip"
    files = [f for f in Path(saves_dir).rglob("*") 
             if f.is_file() and not should_ignore(f.relative_to(saves_dir))]
    with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in tqdm(files, desc="Zipping backup"):
            zipf.write(file, file.relative_to(saves_dir))
    print(f"Backup saved to {backup_file}")

    clean_backups_folder(backup_dir, keep=5)

def safe_copy(src, dst):
    try:
        shutil.copy2(src, dst)
    except OSError:
        shutil.copy(src, dst)
        # Preserve modification time separately
        mtime = os.path.getmtime(src)
        os.utime(dst, (mtime, mtime))

def md5_hash(filepath, chunk_size=8192):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_transfer_paths(base_path):
    base_path = Path(base_path)
    saves_path = base_path
    states_path = None
    parent = base_path.parent
    for folder_name in ['states', 'States']:
        candidate = parent / folder_name
        if candidate.is_dir():
            states_path = candidate
            break
    return saves_path, states_path

def sync_saves(src_dir, dst_dir, dryrun=False):
    print(f"Syncing saves from {src_dir} to {dst_dir}...")
    src_dir, dst_dir = Path(src_dir), Path(dst_dir)
    files = [f for f in src_dir.rglob("*") if f.is_file() and not should_ignore(f.relative_to(src_dir))]
    for src_file in tqdm(files, desc="Copying saves"):
        rel_path = src_file.relative_to(src_dir)
        if 'backup' in rel_path.parts or 'backups' in rel_path.parts:
            continue
        dst_file = dst_dir / rel_path

        src_size = src_file.stat().st_size
        dst_size = dst_file.stat().st_size if dst_file.exists() else -1

        need_copy = False
        if not dst_file.exists():
            need_copy = True
        elif src_size != dst_size:
            need_copy = True
        else:
            # Check hashes for files of same size
            src_hash = md5_hash(src_file)
            dst_hash = md5_hash(dst_file)
            if src_hash != dst_hash:
                need_copy = True

        if need_copy:
            if dryrun:
                print(f"[Dry Run] Would copy: {rel_path}")
            else:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                safe_copy(src_file, dst_file)
                print(f"Copied: {rel_path}")

    print(f"Sync from {src_dir} to {dst_dir} complete.")

def main():
    parser = argparse.ArgumentParser(description="Sync RetroArch saves and optionally states between Mac and handheld.")
    parser.add_argument("-mp", "--macpath", required=True, help="Path to RetroArch saves on Mac")
    parser.add_argument("-hp", "--handheldpath", required=True, help="Path to RetroArch saves on handheld")
    parser.add_argument("--backup", action="store_true", help="Enable backup before syncing")
    parser.add_argument("--dryrun", action="store_true", help="Perform a dry run without making any changes")
    parser.add_argument("--transfer-states", action="store_true", help="Also transfer states folder found next to saves folder")
    parser.add_argument("-mb", "--macbackup", default=None, help="Backup directory for Mac saves (optional)")
    parser.add_argument("-hb", "--handheldbackup", default=None, help="Backup directory for handheld saves (optional)")

    args = parser.parse_args()

    mac_backup_dir = args.macbackup if args.macbackup else os.path.join(args.macpath, "backups")
    handheld_backup_dir = args.handheldbackup if args.handheldbackup else os.path.join(args.handheldpath, "backups")

    if args.backup:
        backup_saves(args.macpath, mac_backup_dir, dryrun=args.dryrun)
        backup_saves(args.handheldpath, handheld_backup_dir, dryrun=args.dryrun)

    sync_saves(args.macpath, args.handheldpath, dryrun=args.dryrun)
    sync_saves(args.handheldpath, args.macpath, dryrun=args.dryrun)

    if args.transfer_states:
        mac_saves, mac_states = get_transfer_paths(args.macpath)
        handheld_saves, handheld_states = get_transfer_paths(args.handheldpath)

        if mac_states and handheld_states:
            print("Syncing states folders...")
            sync_saves(mac_states, handheld_states, dryrun=args.dryrun)
            sync_saves(handheld_states, mac_states, dryrun=args.dryrun)
        else:
            print("States folder not found on one or both devices; skipping states synchronization.")

if __name__ == "__main__":
    main()

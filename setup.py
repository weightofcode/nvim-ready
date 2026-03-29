import os
import platform
import shutil
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# general >>>>>>>>
COMPATIBLE_UNIX = { "Linux", "Darwin", "FreeBSD" }
COMPATIBLE_WIN  = { "Windows" }
MAX_NUM_BACKUPS     = 10
MIN_NUM_TO_KEEP     = 2

def is_compatible_os(os_name):
    return os_name in COMPATIBLE_UNIX or os_name in COMPATIBLE_WIN

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"NVIM_RUN_ERROR: Command failed: {cmd}")
        sys.exit(e.returncode)

def update_chmod_unix_script(script_path: Path):
    if platform.system() in COMPATIBLE_UNIX:
        if script_path.exists():
            curent_permissions = script_path.stat().st_mode
            script_path.chmod(curent_permissions | stat.S_IXUSR)
            print(f"NVIM_SETUP_INFO: Made {script_path} executable.")
# <<<<<<<< general


# Nvim client >>>>>>>>
def check_nvim_installed():
    try:
        result = subprocess.run(
                ["nvim", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL )
        return result.returncode == 0
    except FileNotFoundError:
        return False
# <<<<<<<< Nvim client


# Nvim config >>>>>>>>
def get_nvim_config_path():
    os_name = platform.system()
    if os_name in COMPATIBLE_WIN:
        localappdata = os.environ.get("LOCALAPPDATA")
        if not localappdata:
            print(f"NVIM_CONFIG_ERROR: LOCALAPPDATA not set.")
            sys.exit(1)
        return Path(localappdata)/"nvim"
    elif os_name in COMPATIBLE_UNIX:
        return Path.home()/".config"/"nvim"
    else:
        print(f"NVIM_CONFIG_ERROR: Unsupported OS: {os_name}")
        sys.exit(1)

def backup_existing_config(target_path):
    if not target_path.exists():
        print(f"NVIM_CONFIG_WARNING: Neovim config path does not exist: {target_path}")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = target_path.parent/"nvim_backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir/f"nvim_backup_{timestamp}"
    print(f"NVIM_CONFIG_INFO: Backing up: {target_path} -> {backup_path}")
    shutil.move(str(target_path), str(backup_path))
    # rotate backups
    backups = sorted(backup_dir.glob("nvim_backup_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if len(backups) >= MAX_NUM_BACKUPS:
        to_remove = backups[MIN_NUM_TO_KEEP:]
        for old_backup in to_remove:
            print(f"NVIM_CONFIG_INFO: Removing old backup: {old_backup}")
            if old_backup.is_dir():
                shutil.rmtree(old_backup)
            else:
                old_backup.unlink()
        print("NVIM_CONFIG_INFO: Old backups removed.")

def deploy_nvim_config(repo_root, target_path):
    print("NVIM_CONFIG_INFO: Deploying Neovim config...")
    target_path.mkdir(parents=True, exist_ok=True)
    allowed_items = ["init.lua", ".editorconfig", "lua"]
    for item in allowed_items:
        src = repo_root/item
        dst = target_path/item
        if not src.exists():
            print(f"NVIM_CONFIG_WARNING: {item} not found, skipping.")
            continue
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    print("NVIM_CONFIG_INFO: Deployment of Neovim config complete.")
# <<<<<<<< Nvim config


def main():
    if not check_nvim_installed():
        print("NVIM_INSTALL_WARNING: Neovim is not installed or not in PATH.")
        print("NVIM_INSTALL_INFO: Attempting installation via setup scripts...")
    else:
        print("NVIM_INSTALL_INFO: Neovim is already installed.")

    repo_root = Path(__file__).resolve().parent
    os_name = platform.system()
    if not is_compatible_os(os_name):
        print(f"NVIM_OS_WARNING: Unsupported OS: {os_name}. Proceed at your own risk.")
        print(f"NVIM_OS_WARNING: Supported OSes are: Windows, Linux, macOS, FreeBSD")
    print(f"NVIM_OS_INFO: Detected OS: {os_name}")

    if os_name in COMPATIBLE_WIN:
        setup_ps1 = repo_root/"setup"/"setup.ps1"
        run_command( [
            "powershell",
            "-ExecutionPolicy", "Bypass",
            "-File", str(setup_ps1)] )
    elif os_name in COMPATIBLE_UNIX:
        setup_sh = repo_root/"setup"/"setup.sh"
        update_chmod_unix_script(setup_sh)
        run_command( ["bash", str(setup_sh)] )
    else:
        print(f"NVIM_OS_ERROR: Unsupported OS: {os_name}. Proceed at your own risk.")
        sys.exit(1)

    target_path = get_nvim_config_path()
    print(f"NVIM_CONFIG_INFO: Target path: {target_path}")
    backup_existing_config(target_path)
    deploy_nvim_config(repo_root, target_path)

if __name__ == "__main__":
    main()

import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


COMPATIBLE_UNIX = { "Linux", "Darwin", "FreeBSD" }
COMPATIBLE_WIN  = { "Windows" }

def is_compatible_os(os_name):
    return os_name in COMPATIBLE_UNIX or os_name in COMPATIBLE_WIN

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"NVIM_CONFIG_ERROR: Command failed: {cmd}")
        sys.exit(e.returncode)

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
    backup_path = target_path.parent/"nvim_backup"/f"nvim_backup_{timestamp}"
    print(f"NVIM_CONFIG_INFO: Backing up existing config to: {target_path}")
    shutil.move(str(target_path), str(backup_path))

def deploy_nvim_config(repo_root, target_path):
    print("NVIM_CONFIG_INFO: Deploying Neovim config...")
    target_path.mkdir(parents=True, exist_ok=True)
    allowed_items = ["init.lua", "lua"]
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


def main():
    repo_root = Path(__file__).resolve().parent
    os_name = platform.system()
    if not is_compatible_os(os_name):
        print(f"NVIM_CONFIG_WARNING: Unsupported OS: {os_name}. Proceed at your own risk.")
        print(f"NVIM_CONFIG_WARNING: Supported OSes are: Windows, Linux, macOS, FreeBSD")
    print(f"NVIM_CONFIG_INFO: Detected OS: {os_name}")

    target_path = get_nvim_config_path()
    print(f"NVIM_CONFIG_INFO: Target path: {target_path}")
    backup_existing_config(target_path)
    deploy_nvim_config(repo_root, target_path)

    if os_name in COMPATIBLE_WIN:
        script = repo_root/"setup"/"setup.ps1"
        run_command( [
            "powershell",
            "-ExecutionPolicy", "Bypass",
            "-File", str(script)] )
    elif os_name in COMPATIBLE_UNIX:
        script = repo_root/"setup"/"setup.sh"
        run_command( ["bash", str(script)] )
    else: 
        print(f"NVIM_CONFIG_ERROR: Unsupported OS: {os_name}. Proceed at your own risk.")
        sys.exit(1)

if __name__ == "__main__":
    main()

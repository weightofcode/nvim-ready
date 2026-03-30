#!/usr/bin/env bash
set -e
echo "NVIM_CONFIG_INFO: Running Unix setup..."

# package manager >>>>>>>>
if command -v apt >/dev/null 2>&1; then
    PKG_MANAGER="apt"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MANAGER="pacman"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
elif command -v brew >/dev/null 2>&1; then
    PKG_MANAGER="brew"
elif command -v pkg >/dev/null 2>&1; then
    PKG_MANAGER="pkg"
else
    echo "NVIM_SETUP_ERROR: No supported package manager found."
    exit 1
fi
echo "NVIM_SETUP_ERROR: Detected package manager: $PKG_MANAGER"
# <<<<<<<< package manager

# install Neovim >>>>>>>>
install_package() {
    pkg_name="$1"
    case $PKG_MANAGER in
        apt)
            sudo apt update
            sudo apt install -y "$pkg_name"
            ;;
        pacman)
            sudo pacman -Sy --noconfirm "$pkg_name"
            ;;
        dnf)
            sudo dnf install -y "$pkg_name"
            ;;
        brew)
            brew install "$pkg_name"
            ;;
        pkg)
            sudo pkg install -y "$pkg_name"
            ;;
    esac
}

if ! command -v nvim >/dev/null 2>&1; then
    echo "NVIM_SETUP_INFO: Installing Neovim..."
    install_package neovim
else
    echo "NVIM_SETUP_INFO: Neovim already installed."
fi

echo "NVIM_SETUP_INFO: Neovim already installed."
# <<<<<<<< install Neovim

# Neovim configuration files

## Overview
- basic settings
- plugin manager
- plugins
- install script (installs nvim, packages, fonts, etc.)
- deploy script (have a clean config for Nvim)
- etc.

## Brief
The aim is to have a "click once - run everywhere" experience.
Yes, even in corporate environments, where restrictions are in place.

## Detailed
More info will follow. Stay tuned.



## Live notes (volatile)
### Windows 11 Terminal
#### Neovim Statusline plugin config
- https://github.com/nvim-lualine/lualine.nvim
    - statusline plugin has Nerd Fonts dependencies ( https://www.nerdfonts.com/ )
    - the dependecy is: 
        {
            'nvim-lualine/lualine.nvim', 
            dependencies = { 'nvim-tree/nvim-web-devicons' } <- this line
        }
- nvim-tree/nvim-web-devicons : install with Lazy.nvim (optional)
- make sure to have the nerd font of your choice installed on the system
- once font is installed, additional configuration Terminal is required:
    - Terminal -> Settings -> settings.json file
    - profile -> defaults -> font:
        "font": 
        {
            "face": "Google Sans Code, JetBrainsMono Nerd Font Mono",
            "size": 13
        },
    - save JSON -> restart the terminal
    - JetBrainsMono Nerd Font Mono was used for devicons 
        because Google Sans Code does not have a Nerd Font variant
    
### Install Neovim principles
* Make sure:
    - Nvim is installed
    - Git is installed
* Handle:
    - Linux (multiple package managers)
    - macOS (brew)
    - BSD (pkg)
    - Windows (winget)
* Install only if missing    
* Assume package manager

### What happened under the hood
* fzf - installed with winget (or choco)
* ripgrep - installed with choco

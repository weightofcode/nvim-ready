return {
    -- there is no "native" Lua config, so we adapted the existing Packer config
    -- it looks for files or patterns to calculate project root dir
    -- these are configurable
    "ahmedkhalf/project.nvim",
    init = function()
        require("project_nvim").setup {
            -- your configuration comes here
            -- or leave it empty to use the default settings
            -- refer to the configuration section below
        }
    end
}

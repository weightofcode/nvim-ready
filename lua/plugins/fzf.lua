return {
    "ibhagwan/fzf-lua",
    -- optional for icon support
    dependencies = { "nvim-tree/nvim-web-devicons" },
    -- or if using mini.icons/mini.nvim
    -- dependencies = { "nvim-mini/mini.icons" },
    ---@module "fzf-lua"
    ---@type fzf-lua.Config|{}
    ---@diagnostic disable: missing-fields
    opts = {},
    keys = {
        -- the reason for keybinds here and no in the ususal options.lua/vim
        -- is because nvim will know that these keys are associated with Lazy
        -- and will only load them on demand (performance increase)
        {
            "<leader>ff",
            function() require("fzf-lua").files() end,
            desc="Find Files in project directory"
        },
        {
            "<leader>fg",
            function() require("fzf-lua").live_grep() end,
            desc="Find Files with Grep in project directory"
        },
        {
            "<leader>fc",
            function() require("fzf-lua").files({cwd=vim.fn.stdpath("config")}) end,
            desc="Find Files in config folder of the project directory"
        },
    }
    ---@diagnostic enable: missing-fields
}

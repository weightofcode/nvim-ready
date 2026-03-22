return {
    "rebelot/kanagawa.nvim",
    config=function()
        require('kanagawa').setup({
            compile=true,
            transparent=true,   -- not working in Win11 Terminal
        });
        -- vim.cmd("KanagawaCompile"); -- compile already enabled on line 5
        vim.cmd("colorscheme kanagawa");
    end,
    -- build = function()
    --     vim.cmd("KanagawaCompile");
    -- end,
}

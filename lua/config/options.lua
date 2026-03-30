-- ---------------------------------------
-- Basic General Configuration
-- ---------------------------------------

vim.opt.termguicolors = false   -- attempt to use terminal colors instead of colorschemes

vim.opt.expandtab = true        -- convert tabs to spaces
vim.opt.shiftwidth = 4          -- amount to indent with << and >>
vim.opt.tabstop = 4             -- number of spaces in one Tab
vim.opt.softtabstop = 4         -- number of spaces applied when pressing Tab
vim.opt.smarttab = true         -- delete one Tab at once, not individual spaces
vim.opt.smartindent = true      -- more or less as above, but when pressing CR
vim.opt.autoindent = true       -- keep indentation from the previous line
vim.opt.breakindent = true      -- break indent when line is longer than screen space

vim.opt.number = true           -- line number
vim.opt.cursorline = true       -- highlight cursor line

vim.opt.undofile = true         -- store undo between sessions
vim.opt.mouse = "a"             -- enable mouse
vim.opt.showmode = false        -- don't show the mode, it's already in the statusline

vim.opt.ignorecase = true       -- case-insensitive search
vim.opt.smartcase = true        -- case-sensitive search if a Capital letter is inserted

vim.opt.signcolumn = "yes"      -- vertical column for utils (warning, error, etc.) next to line num

vim.opt.splitright = true       -- make split to the right intuitive
vim.opt.splitbelow = true       -- make split below intuitive

vim.opt.list = true             -- display special characters
vim.opt.listchars = { tab = "≫ ", trail = "·", nbsp = "␣" }

vim.opt.scrolloff = 5           -- minimum number of lines to keep above and below the cursor

-- highlight yanked text for better visibility
vim.api.nvim_create_autocmd("TextYankPost", {
    group = vim.api.nvim_create_augroup("YankHighlight", { clear = true }),
    pattern = "*",
    callback = function()
        vim.highlight.on_yank()
    end,
    desc = "Highlight yank",
})

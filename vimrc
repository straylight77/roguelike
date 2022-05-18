set nocompatible
filetype off

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" --------------------------------------------------------------
" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

Plugin 'chriskempson/base16-vim'

" --------------------------------------------------------------
" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required


set number
set ts=4
set autoindent 
set expandtab
set shiftwidth=4
"set cursorline
set showmatch
let python_highlight_all = 1

syntax enable
colorscheme base16-default-dark
set termguicolors

set laststatus=2



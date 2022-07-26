set nocompatible              " required
set number
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

Plugin 'tmhedberg/SimpylFold'

Plugin 'preservim/nerdtree'

Plugin 'vim-airline/vim-airline'

" Plugin 'vim-syntastic/syntastic'
Plugin 'dense-analysis/ale'

Plugin 'nvie/vim-flake8'

Plugin 'preservim/tagbar'
" add all your plugins here (note older versions of Vundle
" used Bundle instead of Plugin)

" ...

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required


"split navigations
nnoremap <C-M> :split<CR>
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

"split resizing


"NERDTree
nnoremap <C-t> :NERDTreeToggle<CR>

"TagBar
nmap <C-Y> :TagbarToggle<CR>

nnoremap <C-N> :set number!<CR>

"ALE syntax checker toggling
nnoremap <C-A> :ALEToggle<CR>

"autoparentheses
inoremap " ""<left>
inoremap ' ''<left>
inoremap ( ()<left>
inoremap [ []<left>
inoremap { {}<left>

"autocomments
vnoremap <C-c> :norm 0i#<CR>

" Enable folding
set foldmethod=indent
set foldlevel=99


let python_highlight_all=1
syntax on

nnoremap <space> za


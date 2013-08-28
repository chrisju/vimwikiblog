vimwikiblog
===========

make vimwiki a blog

主要是为博客添加评论和代码高亮

> in ~/.vimrc:
    let g:vimwiki_list = [{
    \ 'path': '/mnt/DATA/wiki/wiki/',
    \ 'path_html': '/mnt/DATA/wiki/html/',
    \ 'template_path': '/mnt/DATA/wiki/config/',
    \ 'template_default': 'zz',
    \ 'template_ext': '.tpl',
    \ 'css_name': 'style0.css',
    \ 'auto_export': 1,}]

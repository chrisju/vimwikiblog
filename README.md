vimwikiblog
=========

主要是为博客添加评论和代码高亮

### ~/.vimrc配置
        " 使用鼠标映射
        let g:vimwiki_use_mouse = 1
        
        " 不要将驼峰式词组作为 Wiki 词条
        let g:vimwiki_camel_case = 0
        
        let g:vimwiki_list = [{
        \ 'path': '/mnt/DATA/vimwiki/wiki/',
        \ 'path_html': '/mnt/DATA/vimwiki/html/',
        \ 'template_path': '/mnt/DATA/vimwiki/config/',
        \ 'template_default': 'zz',
        \ 'template_ext': '.tpl',
        \ 'css_name': 'style0.css',
        \ 'auto_export': 1,},{
        \ 'path': '/mnt/DATA/wiki/',
        \ 'path_html': '/mnt/DATA/vimwiki/html/',
        \ 'template_path': '/mnt/DATA/vimwiki/config/',
        \ 'template_default': 'zz',
        \ 'template_ext': '.tpl',
        \ 'css_name': 'style0.css',
        \ 'auto_export': 1,}]


### TODO
> css布局,增加必要元素:header,分类,tag,上下篇
> 外链处理
> 首页
> tag页,分类页,存档页
> 文章时间
> 文章的tag,分类链接
> 页面其它元素

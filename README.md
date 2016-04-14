vimwikiblog
=========

> User Guide: [http://blog.zzbalabala.com/blog/vimwikiblog_en.html](http://blog.zzbalabala.com/blog/vimwikiblog_en.html)
>
> 使用说明: [http://blog.zzbalabala.com/blog/vimwikiblog.html](http://blog.zzbalabala.com/blog/vimwikiblog.html)
>
> 补充资料: [静态博客相关](http://blog.zzbalabala.com/blog/static_blog.html)

### 所做工作
> 添加评论和代码高亮
>
> 生成日期,分类,tag页面
>
> 自动上传

### 需设置的配置
> config/config.json 主要配置文件 至少要配置vimwiki文件所在目录,vimwiki的输出目录 另可配置上传用的ftp设置
>
> ~/.vimrc 配置输出目录,html模版等
>
> config/vimwiki.tpl vimwiki的模版文件 至少要更改自己的博客名字和google搜索域名
>
> config/genpage.tpl 至少要更改自己的博客名字和google搜索域名
>
> site/js/disqus.js disqus评论要更改自己的id
>
> site/js/ga.js google analytics要更改自己的id

### 设置完成后的使用方法
> 若第一次运行,用vim打开wiki文件,使用:VimwikiAll2HTML将文件夹下所有wiki文件转为html
>
> 若不是第一次运行,只要单纯的保存wiki文件就行了
>
> 进入vimwikiblog文件夹
>
> 运行命令 python3 tools/vimwiki2blog.py -c config/config.json

### ~/.vimrc配置
见 config/vimrc

### BUG & TODO
见 wiki/todo.wiki

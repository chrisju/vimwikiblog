#!/usr/bin/env python3

import sys, os
import shutil
import re



#config file
s = ''
with open('config/config.json') as f:
    s = f.read()
s = re.sub(r'("user":").*?(")',r'\g<1>xxx\g<2>', s)
s = re.sub(r'("pwd":").*?(")',r'\g<1>xxx\g<2>', s)
s = re.sub(r'("enable":).*?(,)',r'\g<1>false\g<2>', s)
with open('config/config.json','w') as f:
    f.write(s)


#genpage.tpl
s = ''
with open('config/genpage.tpl') as f:
    s = f.read()
s = re.sub(r'伊谢尔伦的一角',r'xxx', s)
s = re.sub(r'zzbalabala.com',r'xxx.com', s)
s = re.sub(r'chris zz',r'xxx', s)
with open('config/genpage.tpl','w') as f:
    f.write(s)

#vimwiki.tpl
s = ''
with open('config/vimwiki.tpl') as f:
    s = f.read()
s = re.sub(r'伊谢尔伦的一角',r'Blog name', s)
s = re.sub(r'zzbalabala.com',r'xxx.com', s)
s = re.sub(r'chris zz',r'xxx', s)
with open('config/vimwiki.tpl','w') as f:
    f.write(s)

#disqus
s = ''
with open('site/js/disqus.js') as f:
    s = f.read()
s = re.sub(r"(var disqus_shortname = ').*?(')",r'\g<1>xxx\g<2>', s)
with open('site/js/disqus.js','w') as f:
    f.write(s)

#google-analytics
s = ''
with open('site/js/ga.js') as f:
    s = f.read()
s = re.sub(r"(ga\('create', ').*?(', ').*?(')",r'\g<1>xxx\g<2>xxx.com\g<3>', s)
with open('site/js/ga.js','w') as f:
    f.write(s)




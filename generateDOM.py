import os
import re

# this use forgenerate dome element 

print('Generate chart js ...')


for subdir, dirs, files in os.walk('./elementHTML_export'):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".html"):
            contentdiv = open(filepath, 'r').read()
            rel = re.match(r"<div>(?P<domelement>(.|\n)*?)<script(.|\n)*?>(?P<domscr>(.|\n)*?)<\/script>(.|\n)*?<\/div>"
            ,contentdiv)
            #url.removesuffix('.com') 

import os
import re
from bs4 import BeautifulSoup

# this use forgenerate dome element 

print('Embed chart js ...')



soup = BeautifulSoup(open('..\public\index.html','r'), 'html.parser')


for subdir, dirs, files in os.walk('./elementHTML_export'):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".html"):
            contentdiv = open(filepath, 'r').read()
            rel = re.match(r"<div>(?P<domelement>(.|\n)*?)<script(.|\n)*?>(?P<domscr>(.|\n)*?)<\/script>(.|\n)*?<\/div>"
            ,contentdiv)
            #write script 
            with open('..\public\chartjs'+os.sep+file.replace('.html','.js'), 'w') as scriptF:
             scriptF.write(rel.group('domscr'))
            #add dome id 
            chartcon = soup.find(id=file.replace('.html','js'))
            
            chartcon.clear()
            
            chartcon.append(BeautifulSoup(rel.group('domelement'), 'html.parser'))

            print('Append {} complete !'.format(file.replace('.html','js')))


# write back to file
with open("..\public\index.html", "w") as file:
    file.write(str(soup))            
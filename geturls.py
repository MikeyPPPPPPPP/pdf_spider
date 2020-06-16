import time
import bs4 as bs
import urllib.request
import urllib.parse
import re
import os
import requests
import threading


url = "http://index-of.co.uk/"
os.mkdir('layer2')
os.mkdir('layer3')

layer1 = []
layer2 = open(r"layer2/2deep.txt","w")#[]
layer25 = []
layer3 = []
layer4 = open(r"layer3/3deep.txt","w")#[]



def download_file(url):
    local_filename = url.split('/')[-1]# gets 'something.pdf' in http://index-of.co.uk/afds/fasdf.pdf
    # NOTE the stream=True parameter
    local_filename.replace('pbf', 'pdf')
    #print(url)
    #print(file_location+local_filename)
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    
    r = s.get(url, stream=True)
    
    #r = requests.get(url, stream=True)
    with open(r'layer2/'+local_filename, 'wb') as f:#local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

    
def req(url, cat):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    rez = resp.read()

    soup = bs.BeautifulSoup(rez,'lxml')

    for link in soup.findAll('a'):#, attrs={'href'}):
        #print(link.get('href'))
        if 'http://index-of' in link.get('href'):
            pass
        else:
            cat.append(url+link.get('href'))


def req2(url, cat):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        rez = resp.read()

        soup = bs.BeautifulSoup(rez,'lxml')

        for link in soup.findAll('a'):#, attrs={'href'}):
            #print(link.get('href'))
            if link.get('href').endswith('/'):
                layer3.append(url+link.get('href'))

            else:
                cat.write(urllib.parse.unquote(link.get('href')))
                cat.write('\n')
    except Exception as f:
        print('error', f)
        exit()

        
def req1(url, cat):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        rez = resp.read()

        soup = bs.BeautifulSoup(rez,'lxml')

        for link in soup.findAll('a'):#, attrs={'href'}):
            #print(link.get('href'))
            if link.get('href').endswith('/'):
                layer3.append(url+link.get('href'))
                #req2(link.get('href'), layer4)
            else:
                layer25.append(urllib.parse.unquote(url+link.get('href')))
                cat.write(url+link.get('href'))
                cat.write('\n')
                
                
                '''
                try:
                
                    if '.pdf' in link.get('href'):
                        download_file(url+link.get('href'), r'layer2/')
                        #download_file(urllib.parse.unquote(url+link.get('href')), r'layer2/')
                    else:
                        pass
                except Exception as f:
                    print('error', f)
                    print('download error')
                '''
    except Exception as f:
        print('error', f)
        pass



req(url, layer1)


for x in layer1:
    #print(x)
    req1(x, layer2)

layer2.close()
for x in range(0,len(layer25)-1):
    try:
        download_file(layer25[x])
        print(str(x)+'\t'+str(layer25[x])+' Done!')
    except Exception as e:
        print(e)
        
'''
for x in range(0,len(layer25)-1):
    thread = threading.Thread(target=download_file, args=(layer25[x],))
    thread.start()
'''

'''
for x in layer3:
    #print(x)
    req2(x,  'layer3')
'''
layer4.close()

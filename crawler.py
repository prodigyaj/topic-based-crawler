import sys
import os
import Queue
import bs4
import urllib2
import hashlib
import pprint
from random import randint
import time

def bePolite(should_i,random = 2):
    if should_i == True:
        randseed = randint(1,random)
        time.sleep(randomseed)
    

def crawler(depth):
    pp = pprint.PrettyPrinter()
    q = Queue.Queue()
    levelQ = Queue.Queue()
    visited = set()
    file = open("seed.txt")
    domain_reg_file = open("regexseed.txt","r")
    discarded_url_file = open("log/discarded.txt","w")
    visited_url_file = open("log/visted.txt","w")
    exist_url_file = open("log/exist.txt","w")
    exception_file = open("log/exception_logger.txt","w")

    graph_file = open("graph/graph.txt","w")
    key_file   = open("graph/key-value.txt","w")
    seedurl = ""
    domain = []
    for domain_list in domain_reg_file:
        domain.append(domain_list.strip())
    for url in file:
        seedurl = url.strip()
        q.put(seedurl)
        levelQ.put(int(0))

    while not q.empty():
        try:
            url = q.get()
            level = levelQ.get()
            if(level > depth):
                break

            try:
                hex = hashlib.sha224(url).hexdigest()
                key_file.write(hex[:16]+"\t"+url+"\n")
                filename = "cached/"+hex[:16]+".cached"
                print filename

            except:
                exception_file.write("Exception in md5 for url",url)
                continue

            if os.path.isfile(filename):
                try:
                    exist_url_file.write(url+"\n")
                    content = open(filename).read().decode('utf8')
                except:
                    exception_file.write("Exception in opening existing file:",url,filename)
                    continue

            else:
                try:
                    webpage = urllib2.urlopen(url)
                    content = webpage.read().decode('utf8')
                except:
                    exception_file.write("Exception in reading contents of file in web:",url)
                    continue

                #content = open("index.html").read().decode('utf8')
                try:
                    filenew = open(filename,"w")
                    filenew.write("url:"+url+"\n"+content.encode("ascii","ignore"))
                    filenew.close()
                except:
                    exception_file.write("Exception in writing a cached file:",url,filename)
                    continue

            try:
                soup = bs4.BeautifulSoup(content)
                visited.add(url)
            except:
                exception_file.write("Exception in beautiful soup reading content:",url,filename)
                continue

            try:
                for anchor in soup.find_all('a'):
                    #print(anchor.get('href', '/'))
                    import urlparse
                    newurl = urlparse.urljoin(seedurl,anchor.get('href', '/')).strip()
                    text = anchor.text.strip()
                    #print newurl
                    if newurl not in visited:
                        for domain_url in domain:
                            from urlparse import urlparse
                            if urlparse(domain_url).netloc in urlparse(newurl).netloc:
                                #print urlparse(domain_url).netloc
                                visited.add(newurl)
                                levelQ.put(level+1)
                                graph_file.write(url+":==:"+text+":==:"+newurl+"\n")
                                q.put(newurl)
                            else:
                                discarded_url_file.write(newurl+"\n")
                #print webpage
                #print pp.pprint(visited)
                pprint.pprint("level: "+str(level),visited_url_file)
                pprint.pprint(visited,visited_url_file)
                if not os.path.isfile(filename):
                    bePolite(true,3)
            except:
                exception_file.write("Exception in finding anchor tags:",url,filename)
                continue
        except:
            exception_file.write("GLOBAL EXCEPTION")
    discarded_url_file.close()
    visited_url_file.close()
    exist_url_file.close()
    graph_file.close()
    key_file.close()
    exception_file.close()
        

if __name__ == "__main__":
    depth = sys.argv[1]
    crawler(int(depth))

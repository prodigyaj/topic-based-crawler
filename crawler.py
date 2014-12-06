import sys
import os
import Queue
import bs4
import urllib2
import hashlib
import pprint


def crawler(depth):
    pp = pprint.PrettyPrinter()
    q = Queue.Queue()
    levelQ = Queue.Queue()
    visited = set()
    file = open("seed.txt")
    discarded_url_file = open("log/discarded.txt","w")
    visited_url_file = open("log/visted.txt","w")
    exist_url_file = open("log/exist.txt","w")

    graph_file = open("graph/graph.txt","w")
    key_file   = open("graph/key-value.txt","w")
    seedurl = ""
    for url in file:
        seedurl = url.strip()
        q.put(seedurl)
        levelQ.put(int(0))

    while not q.empty():
        url = q.get()
        level = levelQ.get()
        if(level > depth):
            break

        hex = hashlib.sha224(url).hexdigest()
        key_file.write(hex[:16]+"\t"+url)
        filename = "cached/"+hex[:16]+".cached"
        print filename

        if os.path.isfile(filename):
            exist_url_file.write(url+"\n")
            content = open(filename).read().decode('utf8')
        else:
            webpage = urllib2.urlopen(url)
            content = webpage.read().decode('utf8')
            #content = open("index.html").read().decode('utf8')
            filenew = open(filename,"w")
            filenew.write("url:"+url+"\n"+content.encode("ascii","ignore"))
            filenew.close()

        soup = bs4.BeautifulSoup(content)
        visited.add(url)
        for anchor in soup.find_all('a'):
            #print(anchor.get('href', '/'))
            import urlparse
            newurl = urlparse.urljoin(seedurl,anchor.get('href', '/')).strip()
            text = anchor.text.strip()
            #print newurl
            if newurl not in visited:
                from urlparse import urlparse
                if urlparse(seedurl).netloc in urlparse(newurl).netloc:
                    visited.add(newurl)
                    levelQ.put(level+1)
                    graph_file.write(url+":==:"+text+":==:"+newurl+"\n")
                    q.put(newurl)
                else:
                    discarded_url_file.write(newurl+"\n")
        #print webpage
        #print pp.pprint(visited)
        pprint.pprint(visited,visited_url_file)
    discarded_url_file.close()
    visited_url_file.close()
    exist_url_file.close()
    graph_file.close()
    key_file.close()

if __name__ == "__main__":
    depth = sys.argv[1]
    crawler(int(depth))

from config import *
import sys
sys.path.append(beautiful_soup_path)
import os
import Queue
import bs4
import urllib2
import hashlib
import pprint
from random import randint
import time
from live_faculty_predictor import *


def snapshot_crawler(depth,directory=""):
    faculty_link_file = open("faculty_link","w")
    other_link_file = open("other_link","w")
    pred = FacultyPredictor()
    q = Queue.Queue()
    aq = Queue.Queue()
    lq = Queue.Queue()
    visited = set()
    start = open("seed.txt").read().strip()
    domain_reg_file = open("regexseed.txt","r")
    seedurl = start
    q.put(start)
    aq.put("")
    lq.put(int(0))

    exception_file = open("exception_logger.txt","w")


    domain = []
    for domain_list in domain_reg_file:
        domain.append(domain_list.strip())

    while not q.empty():
        try:
            url = q.get()
            anchor_append = aq.get()
            level = lq.get()
            if(level > depth):
                break

            try:
                hex = hashlib.sha224(url).hexdigest()
                filename = hex[:16]+".cached"
                file_path = os.path.join(directory,filename)
                #print file_path

            except:
                #exception_file.write("Exception in md5 for url",url)
                print "Exception in md5 for url",url
                continue

            if os.path.isfile(file_path):
                try:
                    content = open(file_path).read().decode('utf8')
                    soup = bs4.BeautifulSoup(content)
                    for script in soup(["script", "style"]):
                        script.extract()
                    clean_content = soup.get_text()
                    label= pred.predict_label(clean_content)
                    #print file_path
                    if label == 0:
                        #print "result:",anchor_append,":done"
                        faculty_link_file.write(anchor_append+"\n")
                    else:
                        other_link_file.write(anchor_append+"\n")
                except:
                    exception_file.write("Exception in opening existing file:",url,filename)
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
                    anchor_concat = anchor_append + "<:=:=:>" + text
                    #print newurl
                    if newurl not in visited:
                        for domain_url in domain:
                            from urlparse import urlparse
                            if urlparse(domain_url).netloc in urlparse(newurl).netloc:
                                #print urlparse(domain_url).netloc
                                visited.add(newurl)
                                lq.put(level+1)
                                aq.put(anchor_concat.strip())
                                q.put(newurl)
            except:
                exception_file.write("Exception in finding anchor tags:",url,filename)
                continue


        except:
            print "Global Break"
            break

    faculty_link_file.close()
    #print pred.predict_label("professor")


if __name__ == "__main__":
    depth = sys.argv[1]
    #crawler(int(depth))
    snapshot_crawler(depth,snapshot_location)

from config import *
import sys
sys.path.append(beautiful_soup_path)

import os
import bs4

debug = 0

for directory in os.listdir(training_data_location):
    if not os.path.exists(extract_output_location+directory):
        os.makedirs(extract_output_location+directory)

if debug:
    file = open("/srv/data/anair10/cs598/data/webkb/projecthttp:^^www.ai.mit.edu^projects^muscle^muscle.html")
    file = open("/srv/data/anair10/cs598/data/webkb/staff/http:^^www.cs.columbia.edu^~manu^","r")
    soup = bs4.BeautifulSoup(file.read())
    print soup.get_text()
else:
    for directory in os.listdir(training_data_location):
        for html_file in os.listdir(training_data_location+directory):
            try:
                path = os.path.join(training_data_location,directory)
                unclean_file_path = os.path.join(path,html_file)
                unclean_file = open(unclean_file_path,"r")

                soup = bs4.BeautifulSoup(unclean_file.read())
                new_path = os.path.join(extract_output_location,directory)
                new_file_path = os.path.join(new_path,html_file)
                clean_file = open(new_file_path,"w")
                clean_file.write(soup.get_text())
                clean_file.close()

            except:
                print "Unexpected error:", sys.exc_info()[0]
                print "error in ",os.path.join(training_data_location+directory+html_file)
                continue

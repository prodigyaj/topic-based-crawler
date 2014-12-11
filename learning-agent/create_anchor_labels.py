import string
anchor_link = open("faculty_link","r")
faculty = open("faculty_label","w")
exclude = set(string.punctuation)

for line in anchor_link:
    for anchor in line.strip().split("<:=:=:>"):
        if len(anchor.strip()) > 2:
            anchor = ''.join(ch for ch in anchor if ch not in exclude)
            for words in anchor.split():
                faculty.write(words+"\t1\n")
'''
anchor_link = open("other_link","r")
exclude = set(string.punctuation)

for line in anchor_link:
    for anchor in line.strip().split("<:=:=:>"):
        if len(anchor.strip()) > 2:
            anchor = ''.join(ch for ch in anchor if ch not in exclude)
            for words in anchor.split():
                faculty.write(words+"\t0\n")
                #print words
'''

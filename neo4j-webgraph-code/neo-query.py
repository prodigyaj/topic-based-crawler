file = open("graph.txt","r")
dict = {}
node = 1
for line in file:
    try:
        old,anchor,new = line.strip().split(":==:")
        if dict.get(old,0) == 0:
            dict[old]=node
            #print "CREATE (urlnode_"+str(node)+":UrlNode {url:'"+old+"', nodenumber:"+str(node)+"});"
            print "CREATE (n:UrlNode {url:'"+old+"', nodenumber:"+str(node)+"});"
            node = node + 1
        if dict.get(new,0) == 0:
            dict[new]=node
            #print "CREATE (urlnode_"+str(node)+":UrlNode {url:'"+new+"', nodenumber:"+str(node)+"});"
            print "CREATE (n:UrlNode {url:'"+new+"', nodenumber:"+str(node)+"});"
            node = node + 1
    except:
        continue
file.close()
file = open("graph.txt","r")
for line in file:
    try:
        old,anchor,new = line.strip().split(":==:")
        anchor = anchor.replace("'","")
        print "MATCH (a:UrlNode),(b:UrlNode)"
        print "WHERE a.nodenumber = "+str(dict[old])+" AND b.nodenumber = "+str(dict[new])
        print "CREATE (a)-[:OutLink {anchor_text:['"+anchor+"']}]->(b);"
    except:
        continue

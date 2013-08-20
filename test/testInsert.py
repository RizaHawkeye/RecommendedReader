import json
import database

f=open("getReadContent.txt")
unreadContent=f.read()

result=json.loads(unreadContent)

title = result["items"][0]["title"]
content = result["items"][0]["summary"]["content"]
href = result["items"][0]["canonical"][0]["href"]
author = result["items"][0]["author"]
timestampUsec = result["items"][0]["timestampUsec"]

title.replace("'","''")
content.replace("'","''")
href.replace("'","''")
author.replace("'","''")
timestampUsec.replace("'","''")
website = "DOUBAN"



#print "title----------------" + title
#print "content--------------" + content		
#print "author--------------" + author		
#print "href--------------" + href		

db = database.Database()

sql = "delete from Articals"
db.executeWithoutQuery(sql)

sql = '''insert into Articals(id,author,title,website,content,href,timestampUsec) values('%s','%s','%s','%s','%s','%s','%s')''' % (id,author,title,website,content,href,timestampUsec)
db.executeWithoutQuery(sql)

sql = "select * from Articals"
res = db.query(sql)

title = res[0]["id"]
content = res[0]["content"]
href = res[0]["href"]
author = res[0]["author"]
timestampUsec = res[0]["timestampUsec"]

print "title----------------" + title
print "content--------------" + content		
print "author--------------" + author		
print "href--------------" + href		



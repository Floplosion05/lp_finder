import sqlite3
from urllib.request import pathname2url

connector = sqlite3.connect(f"file:{pathname2url('lps.db')}?mode=rw")
connector2 = sqlite3.connect(f"file:{pathname2url('lps2.db')}?mode=rwc")
connector2.execute("CREATE TABLE lps (id INTEGER NOT NULL PRIMARY KEY ASC, lp_id INTEGER UNIQUE, name TEXT, lat DOUBLE, long DOUBLE, city TEXT, category INTEGER, description TEXT, title_pic_url TEXT)")
connector2.execute("CREATE TABLE IF NOT EXISTS pics (pic_id INTEGER PRIMARY KEY, lp_id INTEGER, url TEXT, FOREIGN KEY(lp_id) REFERENCES lps(lp_id))")
connector2.execute("CREATE TABLE IF NOT EXISTS comments (comment_id INTEGER PRIMARY KEY, lp_id INTEGER, content TEXT, date DATE, username TEXT,FOREIGN KEY(lp_id) REFERENCES lps(lp_id))")
connector.row_factory = sqlite3.Row
cursor = connector.cursor()
cursor.execute("SELECT * from lps")
lps = [dict(r) for r in cursor.fetchall()]
for lp in lps:
	lp["title_pic_url"] = lp["title_pic_url"].replace("https://", "https://lostplace.club")
	connector2.execute("INSERT INTO lps (id, lp_id, name, lat, long, city, category, description, title_pic_url) VALUES (?,?,?,?,?,?,?,?,?)", (None, lp["lp_id"], lp["name"], lp["lat"], lp["long"], lp["city"], lp["category"], None, lp["title_pic_url"]))
connector2.commit()
cursor.execute("SELECT * from pics")
pics = [dict(r) for r in cursor.fetchall()]
for pic in pics:
	connector2.execute("INSERT INTO pics (pic_id, lp_id, url) VALUES (?,?,?)", (None, pic["lp_id"], pic["url"]))
connector2.commit()
cursor.execute("SELECT * from comments")
comments = [dict(r) for r in cursor.fetchall()]
for comment in comments:
	connector2.execute("INSERT INTO comments (comment_id, lp_id, content, date, username) VALUES (?,?,?,?,?)", (None, comment["lp_id"], comment["content"], comment["date"], comment["username"]))
connector2.commit()
connector2.close()

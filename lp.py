import sqlite3
from flask import Flask, render_template, g
app=Flask("Lp.py", )

DATABASE = "lps.db"
markers = []
ids = []

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return "Lp.py"

@app.route("/<int:Number>")
def allow(Number):
    if Number in ids:
        lp_cur = get_db().cursor()
        lp_cur.execute("SELECT * from lps WHERE id=?",(str(Number),))
        lp = dict(lp_cur.fetchone())
        lp_cur.execute("SELECT * from comments WHERE lp_id=(SELECT lp_id from lps WHERE id=(?))",(str(Number),))
        comments = [dict(r) for r in lp_cur.fetchall()]
        lp_cur.execute("SELECT * from pics WHERE lp_id=(SELECT lp_id from lps WHERE id=(?))",(str(Number),))
        pics = [dict(r) for r in lp_cur.fetchall()]
        lp_cur.close()
        return render_template("lp.html", lp=lp, comments=comments, pics=pics)
    else:
       return f"No lp found with specified id: {str(Number)}"

@app.route('/map')
def root():
    return render_template('map.html', markers=markers)

with app.app_context():
    cur = get_db().cursor()
    cur.execute("SELECT id,name,lat,long,category,title_pic_url,(SELECT COUNT(url) FROM pics WHERE lp_id=lps.lp_id) as pic_count,(SELECT COUNT(content) FROM comments WHERE lp_id=lps.lp_id) as comment_count from lps;")
    markers = {dict(r)["id"]:dict(r) for r in cur.fetchall()}
    ids = markers.keys()
    cur.close()

if __name__ == "__main__":
    app.run(host="localhost", port=8080)

# url parameter
# Leaflet.Locate
# tunnel zrok, ngrok?
# window fullscreen
# pic und comment count in scrape skript

# []
# {}
# \

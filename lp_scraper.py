# pylint: disable=line-too-long

"""
lp_scraper.py

A script to automatically scrape lp's from existing databases
"""

import sqlite3
import time
from datetime import datetime
from urllib.request import pathname2url
import argparse
from enum import Enum
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

Category = Enum("Category",[
    "Industrie",
    "Hotel",
    "Schule",
    "Medizinisch",
    "Militär",
    "Bunker",
    "Haus",
    "Religiös",
    "Unterhaltung",
    "Verkehr",
    "Landwirtschaft",
    "Ruine",
    "Sonstiges"
])

def formatter(prog):
    r"""Formats the help display of the script to have a certain width
    """

    return argparse.HelpFormatter(prog, max_help_position=64)

def parseargs():
    r"""Parses the args and returns them as a dictionary
    """

    parser = argparse.ArgumentParser(
                        prog="lp_scraper",
                        description="Script to find lp's in a given radius around a city",
                        formatter_class=formatter,
                        epilog="By @Floplosion05")
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="Whether or not debug mode should be enabled")
    return parser.parse_args()

def lostplace_club(conn, startindex, debug):
    r""""Scrapes the lostplace.club site
    
    :param conn: The connector or cursor object to interact with the database
    :param startindex: The starting id to scrape
    :param debug: Whether or not to print debug output
    """

    error_count = 0

    markers_url = "https://lostplace.club/functions/map/get_markers.php"
    markers_req: requests.Response = requests.get(url=markers_url, timeout=10)
    markers = json.loads(markers_req.text)
    markers = sorted(markers, key=lambda k: k.get("id",0))
    with open("./ressources/markers.txt", "w+", encoding="utf-8") as f:
        f.write(json.dumps(markers, indent=4, ensure_ascii=False))
    markers = {j["id"]:j for j in markers}

    for i in range(startindex,999999):#, desc="lp_scraper.py"):

        print(f"Scraping lp with index: {i}")
        url = f"https://lostplace.club/place.php?id={i}"
        req: requests.Response = requests.get(url=url, timeout=10)
        soup = BeautifulSoup(req.text, "html.parser")
        if "404" in soup.title.text:

            if error_count <= 50:

                error_count += 1
                continue
            break
        try:

            lp_id = soup.css.select_one("body > div.container > section.place__information-container > div.place__main-image > div > div.place__main-image-id").text.strip().replace("#", "")
        except AttributeError:

            continue

        if int(lp_id) == i:

            conn.execute("CREATE TABLE IF NOT EXISTS comments (comment_id INTEGER PRIMARY KEY, lp_id INTEGER, content TEXT, date DATE, username TEXT,FOREIGN KEY(lp_id) REFERENCES lps(lp_id))")
            for j,comment in enumerate(soup.css.select("body > div.container > section.place__comment > a > div.place__comment-container > div.place__comment-container-flex > div.place__comment-content")):

                content = comment.p.text.strip().replace("\n","").replace("\r","")
                username = soup.css.select("body > div.container > section.place__comment > a > div.place__comment-container > div.place__comment-information")[j].text.split(' - ')[0].strip()
                date_str = soup.css.select("body > div.container > section.place__comment > a > div.place__comment-container > div.place__comment-information")[j].text.split(' - ')[1]
                date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
                if debug:
    
                    print("INSERT INTO comments (comment_id, lp_id, content, date, username) VALUES", (None, lp_id, content, date_obj, username))

                conn.execute("INSERT INTO comments (comment_id, lp_id, content, date, username) VALUES (?,?,?,?,?)", (None, lp_id, content, date_obj, username))

            conn.execute("CREATE TABLE IF NOT EXISTS pics (pic_id INTEGER PRIMARY KEY, lp_id INTEGER, url TEXT, FOREIGN KEY(lp_id) REFERENCES lps(lp_id))")

            gallery_url = f"https://lostplace.club/gallery.php?id={i}"
            gallery_req: requests.Response = requests.get(url=gallery_url, timeout=10)
            gallery_soup = BeautifulSoup(gallery_req.text, 'html.parser')
            if len(gallery_soup.css.select_one("body > div.gallery > div#gallery__container").contents) > 1:

                for pic in gallery_soup.css.select("body > div.gallery > div#gallery__container > img"):

                    url = pic["src"]
                    if debug:

                        print("INSERT INTO pics (pic_id, lp_id, url) VALUES", (None, lp_id, url))

                    conn.execute("INSERT INTO pics (pic_id, lp_id, url) VALUES (?,?,?)", (None, lp_id, url))
            else:

                if debug:

                    print("No pics for lp")

            title_pic_url = soup.css.select_one("div.place__main-image")["style"].split("url('.")[1].split("')")[0].strip()
            title_pic_url = f"https://lostplace.club{title_pic_url}"
            category = markers[int(lp_id)].get("category", 0)
            name = soup.css.select_one("body > div.container > section.place__information-container > div.place__information-flex-container > div.place__information-column > div.place__information-heading").text.strip()
            city = soup.css.select_one("body > div.container > section.place__information-container > div.place__information-flex-container > div.place__information-column > div.place__information-text").text.strip()
            coords = tuple(soup.css.select_one(".bi-globe-americas").parent["href"].split("@")[1][::-1].split(",",1)[1][::-1].split(","))
            if debug:

                print("INSERT INTO lps (id, lp_id, name, lat, long, city, category, description, title_pic_url) VALUES", (None, lp_id, name, coords[0], coords[1], city, category, None, title_pic_url))

            conn.execute("INSERT INTO lps (id, lp_id, name, lat, long, city, category, description, title_pic_url) VALUES (?,?,?,?,?,?,?,?,?)", (None, lp_id, name, coords[0], coords[1], city, category, None, title_pic_url))
        else:

            if debug:

                print(f"Mismatch {lp_id}:{i} (lp_id:i)")

        if int(lp_id)%15 == 0:

            conn.commit()

def lostplace_map(conn):
    r"""Scrapes the lostplace_map.com site
    """

    url: str = "https://lostplace-map.com/"
    req: requests.Response = requests.get(url=url, timeout=10)
    soup = BeautifulSoup(req.text, "html.parser")
    scripts = soup.find_all("script")
    for script in scripts:

        if 'new Array("test")' in script.text:

            json_str = script.text.split("var data = '")[1].split("'; // Platzhalter")[0]
            json_obj = json.loads(json_str)

    urls = []
    for lp in json_obj:

        lp_json_soup = BeautifulSoup("<a"+lp["properties"]["description"].split("<a")[1], "html.parser")
        urls+=lp_json_soup.css.select_one("a")["href"].replace(r'\"','"')
    
    with open("./ressources/urls.txt", "w+", encoding="utf-8") as f:
        f.writelines(url)

    for url in urls:

        lp_req = requests.get(url)
        lp_soup = BeautifulSoup(lp_req.text, "html.parser")
    #conn.execute("INSERT INTO lps (id, lp_id, name, lat, long, city) VALUES (?,?,?,?,?,?)", (None, None, name, coords[0], coords[1], None))

if __name__ == "__main__":
    args = parseargs()
    print(args.debug)
    t = time.process_time()
    start = 1
    skip_count = 0

    try:

        connector = sqlite3.connect(f"file:{pathname2url('lps.db')}?mode=rw")
        cursor = connector.cursor()
        cursor.execute("SELECT lp_id FROM lps ORDER BY lp_id DESC LIMIT 1")
        last_lp_id = int(cursor.fetchall()[0][0])
        cursor.execute("SELECT id FROM lps ORDER BY id DESC LIMIT 1")
        skip_count = int(cursor.fetchall()[0][0]) - last_lp_id
        print("Using existing database")
        start = last_lp_id+1

    except (sqlite3.OperationalError,IndexError) as e:

        if isinstance(e, sqlite3.OperationalError):

            print("No existing database found")
            connector = sqlite3.connect(f"file:{pathname2url('lps.db')}?mode=rwc")
            cursor = connector.cursor()
            cursor.execute("CREATE TABLE lps (id INTEGER NOT NULL PRIMARY KEY ASC, lp_id INTEGER UNIQUE, name TEXT, lat DOUBLE, long DOUBLE, city TEXT, category INTEGER, description TEXT, title_pic_url TEXT)")
        else:

            print("Failed to use existing database")

    lostplace_club(connector, start, args.debug)
    #lostplace_map(connector)
    cursor.execute("SELECT id FROM lps ORDER BY id DESC LIMIT 1")
    last_id = cursor.fetchall()[0][0]
    connector.commit()
    connector.close()
    print(f"Took {round(time.process_time() - t, 2)}s and database has {last_id} entries")

# []
# {}
# \

#https://lostplace-map.com/gm-place/bahnhof-2/

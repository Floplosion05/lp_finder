import argparse
import requests
from bs4 import BeautifulSoup
#from geopy import distance

def formatter(prog):
    r"""Formats the help display of the script to have a certain width
    """

    return argparse.HelpFormatter(prog, max_help_position=64)

def parseargs() -> dict:
    r"""Parses the args and returns them as a dictionary
    """

    parser = argparse.ArgumentParser(
                        prog="lp_finder",
                        description="Script to find lp's in a given radius around a city",
                        formatter_class=formatter,
                        epilog="By @Floplosion05")
    parser.add_argument("-c", "--city",
                        metavar="<city>",
                        type=str,
                        help="Specify the city to be searched for lp's",
                        nargs=1,
                        required=True)
    parser.add_argument("-r", "--radius",
                        metavar="<radius>",
                        type=int,
                        help="Specify the radius in km (defaults to 10)",
                        nargs="?",
                        default=10)
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="Whether or not debug mode should be enabled")
    return vars(parser.parse_args())

def distance(start_coords : tuple, end_coords : tuple) -> int:
    r"""Returns the distance between two given locations using public roads
    
    :param start_coords:
    :param end_coords
    """
    api: requests.Response = requests.get(url=f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248c7259f9c823e47aaa576f83dea8c410d&start={start_coords[1]},{start_coords[0]}&end={end_coords[1]},{end_coords[0]}", timeout=10)
    print(api.json()["features"][0]["properties"]["summary"]["distance"])

def lostplace_club_soupify(html : str):
    r"""Parses a given html document into a list of lost place dictionaries
    
    :param html: The html to be parsed
    """
    return BeautifulSoup(markup=html, features='html.parser')

def get_coordinates(city : str) -> tuple:
    r"""Retrieves the coordinates of a given city and returns them in a tuple

    :param city: The city of which the coordinates are to be requested
    """

    nominatim_url: str = f"http://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    nominatim_r: requests.Response = requests.get(url=nominatim_url, headers={"User-Agent":"lp_finder"},timeout=10)
    
    return (nominatim_r.json()[0].get("lat"),nominatim_r.json()[0].get("lon"))

def get_lps_lostplace_club(coords : tuple, city_name : str, cached_html_eng=False, cached_html=False, debug = False) -> list:
    r"""Retrieves lp's around given coordinates

    :param coords: The coordinates of the location around which lp's are to be searched
    """
    
    if not cached_html_eng:
        lostplace_club_eng_url: str = f"https://lostplace.club/listview.php?lat={coords[0]}&lon={coords[1]}"
        lostplace_club_eng_r: requests.Response = requests.get(url=lostplace_club_eng_url, timeout=10)
        soup_base_eng = lostplace_club_soupify(html=lostplace_club_eng_r.text)
        lps_html_eng = soup_base_eng.css.select("body > div.container > div.listview2__container > div.listview2__item")
        i=0
        while city_name.lower() in lps_html_eng[-1].css.select_one(".bi-geo").parent.span.text.split(":")[1].lower():
            lostplace_club_eng_url: str = f"https://lostplace.club/listview.php?lat={coords[0]}&lon={coords[1]}&page={i}"
            lostplace_club_eng_r: requests.Response = requests.get(url=lostplace_club_eng_url, timeout=10)
            soup_base_eng = lostplace_club_soupify(html=lostplace_club_eng_r.text)
            lps_html_eng += soup_base_eng.css.select("body > div.container > div.listview2__container > div.listview2__item")
            i+=1
    else:
        soup_base_eng = lostplace_club_soupify(html=cached_html_eng)
        lps_html_eng = soup_base_eng.css.select("body > div.container > div.listview2__container > div.listview2__item")
    
    lps: list = {}
    for lp_html in lps_html_eng:
            if city_name.lower() in lps_html_eng[-1].css.select_one(".bi-geo").parent.span.text.split(":")[1].lower() or debug:
                lp: dict = {}
                id: str = lp_html.css.select_one("div.listview2__item-headline").text.split(" (#")[1].split(")")[0].strip()
                lp.update({"name":lp_html.css.select_one("div.listview2__item-headline").text.split(" (#")[0].strip()})
                lp.update({"coords":(lp_html.css.select_one("i.bi-arrow-bar-right").parent.span.text.split(":")[1].strip(),
                lp_html.css.select_one("i.bi-arrow-bar-up").parent.span.text.split(":")[1].strip())})
                lp.update({"pic_url":f'https://lostplace.club{lp_html.css.select_one("div.listview2__item-picture").get("style").split("url(")[1][2:].split(")")[0][:-1].strip()}'})
                lp.update({"comment_cnt": lp_html.css.select_one(".bi-pencil").parent.span.text.split(":")[1].strip()})
                #lp.update({"dist": lp_html.css.select_one(".bi-cursor").parent.span.text.split(":")[1].strip().split("Kilo")[0].strip()})
                #lp.update({"dist": distance(start_coords=coords,end_coords=lp["coords"])})
                lps.update({id:lp})

    if not cached_html:
        lostplace_club_url: str = f"https://lostplace.club/listenansicht.php?lat={coords[0]}&lon={coords[1]}"
        lostplace_club_r: requests.Response = requests.get(url=lostplace_club_url, timeout=10)
        soup_base = lostplace_club_soupify(html=lostplace_club_r.text)
    else:
        soup_base = lostplace_club_soupify(html=cached_html)

    
    lps_html = soup_base.css.select("body > div > a[href^='./place.php?id=']")
    for lp_html in lps_html:
        id = lp_html.css.select_one(".bi-hash").parent.text.strip()
        if id in lps.keys():
            lps[id].update({"pic_cnt": lp_html.css.select_one(".bi-images").parent.text.strip()})
        #else:
        #    lps[id] = {"Bilder": lp_html.css.select_one(".bi-images").parent.text.strip()}
        #lps.append({"name":lp_html.css.select_one(".listenansicht__top-information-heading").text.strip(),
        #            "id":lp_html.css.select_one(".bi-hash").parent.text.strip(),
        #            "lat":lp_html.css.select_one(".bi-geo-alt").parent.text.split(" - ")[0].strip(),
        #            "lon":lp_html.css.select_one(".bi-geo-alt").parent.text.split(" - ")[1].strip(),
        #            "pic_url":f'https://lostplace.club{lp_html.css.select_one(".listenansicht__image").get("data-bg").strip()}'})

    return lps

def main() -> None:
    r"""Main function
    """
    args: dict = parseargs()
    city_coords: tuple = get_coordinates(city=args["city"][0])
    if args["debug"]:
        with open(file="lost_place_club_eng.txt",mode="r",encoding="utf-8") as fp:
            soup_eng: str = fp.read()
        with open(file="lost_place_club.txt",mode="r",encoding="utf-8") as fp:
            soup: str = fp.read()
        lps: list = get_lps_lostplace_club(coords=city_coords, city_name=args["city"][0], cached_html_eng=soup_eng, cached_html=soup, debug=True)
    else:
        lps: list = get_lps_lostplace_club(coords=city_coords, city_name=args["city"][0])
    print(len(lps))

if __name__ == "__main__":
    main()
    pass

# []
# {}


# filter stadtname, radius

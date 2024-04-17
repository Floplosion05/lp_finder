import argparse
import requests
from bs4 import BeautifulSoup

# class LpBase(object):

    # def __init__(self, lat, lon, name, pic_url) -> None:
        # self.lat: str = lat
        # self.lon: str = lon
        # self.name: str = name
        # self.pic_url: str = pic_url

    # def __str__(self):
        # return self.name

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
    return vars(parser.parse_args())

def lostplace_club_soupify(html : str) -> list:
    r"""Parses a given html document into a list of lost places
    
    :param html: The html to be parsed
    """
    soup_base = BeautifulSoup(markup=html, features='html.parser')
    lps_html = soup_base.css.select("body > div > a[href^='./place.php?id=']")
    lps = []
    for lp_html in lps_html[:5]:
        lps.append({"name":lp_html.css.select_one(".listenansicht__top-information-heading").text.strip(),
                    "lat":lp_html.css.select_one(".bi-geo-alt").parent.text.split(" - ")[0].strip(),
                    "lon":lp_html.css.select_one(".bi-geo-alt").parent.text.split(" - ")[1].strip(),
                    "pic_url":lp_html.css.select_one(".listenansicht__image").get("data-bg").strip(),
                    "id":lp_html.css.select_one(".bi-hash").parent.text.strip()})

        # lps.append(LpBase(lat=lp_html.css.select_one(".bi-geo-alt").parent.text.split(" - ")[0].strip(),
                        #   lon=lp_html.css.select_one(".bi-geo-alt").parent.text.split(" - ")[1].strip(),
                        #   name=lp_html.css.select_one(".listenansicht__top-information-heading").text.strip(),
                        #   pic_url=lp_html.css.select_one(".listenansicht__image").get("data-bg").strip()))

    return[lps]

def lostplace_club_eng_soupify(html : str) -> list:
    r"""Parses a given html document into a list of lost places
    
    :param html: The html to be parsed
    """
    soup_base = BeautifulSoup(markup=html, features='html.parser')
    lps_html = soup_base.css.select("body > div.container > div.listview2__container > div.listview2__item")
    lps = []
    for lp_html in lps_html[:5]:
        print(lp_html.css.select_one("i.bi-arrow-bar-right").parent.span.text.split(":")[1].strip())
        lps.append({"name":lp_html.css.select_one("div.listview2__item-headline").text.split(" (#")[0].strip(),
                    "id":lp_html.css.select_one("div.listview2__item-headline").text.split(" (#")[1].split(")")[0].strip(),
                    "lat":lp_html.css.select_one("i.bi-arrow-bar-right").parent.span.text.split(":")[1].strip(),
                    "lon":lp_html.css.select_one("i.bi-arrow-bar-up").parent.span.text.split(":")[1].strip(),
                    "pic_url":f'https://lostplace.club{lp_html.css.select_one("div.listview2__item-picture").get("style").split("url(")[1][2:].split(")")[0][:-1].strip()}'})
    return[lps]

def get_coordinates(city : str)->tuple:
    r"""Retrieves the coordinates of a given city and returns them in a tuple

    :param city: The city of which the coordinates are to be requested
    """

    nominatim_url: str = f"http://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    nominatim_r: requests.Response = requests.get(url=nominatim_url, headers={"User-Agent":"lp_finder"},timeout=10)
    return (nominatim_r.json()[0].get("lat"),nominatim_r.json()[0].get("lon"))

def get_lps_lostplace_club(lat : str, lon : str)->list:
    r"""Retrieves lp's around given coordinates

    :param lat: The lattitude of the location
    :param lon: The longtitude of the location
    """

    lostplaceclub_url: str = f"https://lostplace.club/listenansicht.php?lat={lat}&lon={lon}"
    lostplaceclub_r: requests.Response = requests.get(url=lostplaceclub_url, timeout=10)
    
    # with open("lost_place_club_eng.txt","w+",encoding="utf-8") as fp:
    #    fp.write(lostplaceclub_r.text )
    
    lps: list = lostplace_club_soupify(html=lostplaceclub_r.text)
    print(lps[:5])

def get_lps_lostplace_club_eng(lat : str, lon : str)->list:
    r"""Retrieves lp's around given coordinates

    :param lat: The lattitude of the location
    :param lon: The longtitude of the location
    """

    lostplaceclub_url: str = f"https://lostplace.club/listview.php?lat={lat}&lon={lon}"
    lostplaceclub_r: requests.Response = requests.get(url=lostplaceclub_url, timeout=10)
    
    # with open("lost_place_club_eng.txt","w+",encoding="utf-8") as fp:
    #    fp.write(lostplaceclub_r.text )
    
    return lostplace_club_eng_soupify(html=lostplaceclub_r.text)

def main():
    r"""Main function
    """
    args: dict = parseargs()
    city_coords: tuple = get_coordinates(city=args["city"])
    lps: list = get_lps_lostplace_club_eng(lat=city_coords[0],lon=city_coords[1])
    # with open(file="lost_place_club_eng.txt",mode="r",encoding="utf-8") as fp:
    #    soup: str = fp.read()
    # lps: list = lostplace_club_soupify(html=soup)
    print(lps[:5])

if __name__ == "__main__":
    main()

# []
# {}

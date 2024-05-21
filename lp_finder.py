import argparse
import requests
import sqlite3
#from geopy import distance

def formatter(prog):
    r"""Formats the help display of the script to have a certain width
    """

    return argparse.HelpFormatter(prog, max_help_position=64)

def parseargs():
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

def get_coordinates(city : str) -> tuple:
    r"""Retrieves the coordinates of a given city and returns them in a tuple

    :param city: The city of which the coordinates are to be requested
    """

    nominatim_url: str = f"http://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    nominatim_r: requests.Response = requests.get(url=nominatim_url, headers={"User-Agent":"lp_finder"},timeout=10)
    
    return (nominatim_r.json()[0].get("lat"),nominatim_r.json()[0].get("lon"))

def main() -> None:
    r"""Main function
    """

    args = parseargs()
    city_coords: tuple = get_coordinates(city=args["city"][0])

if __name__ == "__main__":
    main()
    pass

# []
# {}
# \

# filter stadtname, radius
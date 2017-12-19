from bs4 import BeautifulSoup

import logging
import urllib2

WIKI_URL = "https://en.wikipedia.org"


def scrape_actor(url):
    """ scrape_actor scrapes a wikipedia actor page for actor details
        :param url - the actor url to scrape """

    link = url
    name = ""
    age = 0
    movies = []

    logging.basicConfig(filename="./logs/scrape_actor.log")

    wiki_page = urllib2.urlopen(url).read()
    wiki_actor = BeautifulSoup(wiki_page, "html.parser")
    wiki_actor.prettify()

    wiki_actor_table = wiki_actor.find("table", {"class": "infobox biography vcard"})
    if wiki_actor_table is None:
        logging.warning("actor info table not found; breaking this search")
        return

    wiki_name = wiki_actor_table.find_next("span")
    if wiki_name is None:
        logging.warning("actor name not found")
    else:
        logging.warning("actor name found")
        name = wiki_name.get_text()

    wiki_age = wiki_actor_table.find("span", {"class": "noprint ForceAgeToShow"})
    if wiki_age is None:
        logging.warning("age not found")
    else:
        logging.warning("age found")
        age = parse_age(wiki_age.contents[0])

    wiki_filmography = wiki_actor.find("span", {"id": "Filmography"})
    if wiki_filmography is None:
        logging.warning("filmography section not found")
    else:
        logging.warning("filmography section found; proceeding to find films")
        wiki_films = wiki_filmography.find_next("ul")
        for film in wiki_films.findAll("i"):
            movie_data = film.find("a")
            if movie_data is None:
                logging.warning("movie link is empty")
                return
            movie_name = movie_data.get_text()
            movie_link = WIKI_URL + movie_data.get("href")
            movies.append([movie_name, movie_link])

    actors_json = {
        "link": link,
        "name": name,
        "age": age,
        "movies": movies
    }

    return actors_json


def parse_age(age):
    """ parse_age parses a given age into a useful format
     :param age - the age in it's raw format """

    age = filter(unicode.isdigit, age)
    return int(age)

# print(scrape_actor("https://en.wikipedia.org/wiki/Morgan_Freeman"))

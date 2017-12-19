from bs4 import BeautifulSoup

import logging
import re
import urllib2

WIKI_URL = "https://en.wikipedia.org"


def scrape_movie(url):
    """ scrape_movie scrapes a wikipedia movie page for movie details
        :param url - the movie url to scrape """

    link = url
    name = ""
    year = 0
    gross = 0
    cast = []

    logging.basicConfig(filename="./logs/scrape_movie.log")

    wiki_page = urllib2.urlopen(url).read()
    wiki_movie = BeautifulSoup(wiki_page, "html.parser")
    wiki_movie.prettify()

    wiki_movie_table = wiki_movie.find("table", {"class": "infobox vevent"})
    if wiki_movie_table is None:
        logging.warning("movie info table not found; breaking this search")
        return

    wiki_name = wiki_movie_table.find("th", {"class": "summary"})
    if wiki_name is None:
        logging.warning("movie name not found")
    else:
        logging.warning("movie name found")
        name = wiki_name.text

    wiki_date = wiki_movie_table.find("span", {"class": "bday dtstart published updated"})
    if wiki_date is None:
        logging.warning("movie release date not found")
    else:
        logging.warning("movie release date found")
        year = parse_year(wiki_date.contents[0])

    wiki_gross = wiki_movie_table.find(text=re.compile("Box office"))
    if wiki_gross is None:
        logging.warning("movie gross not found")
    else:
        logging.warning("movie gross found")
        wiki_gross = wiki_gross.find_next("td").contents[0]
        gross = parse_gross(wiki_gross)

    wiki_starring = wiki_movie_table.find(text=re.compile("Starring"))
    if wiki_starring is None:
        logging.warning("movie starring list not found")
    else:
        logging.warning("movie starring list found")
        wiki_starring = wiki_starring.find_next("ul")
        count = 0
        for wiki_cast in wiki_starring.findAll("a"):
            cast_name = wiki_cast.get_text()
            cast_link = WIKI_URL + wiki_cast.get("href")
            cast_weight = count + 1
            count += 1
            cast.append([(cast_name), (cast_link), (cast_weight)])

    movies_json = {
        "link": link,
        "name": str(name),
        "year": year,
        "gross": gross,
        "cast": cast
    }

    return movies_json


def parse_gross(gross):
    """ parse_gross parses a raw format of gross to a useful format
        :param gross - the gross in it's raw format """

    gross = gross.replace("[", "")
    gross = gross.replace("$", "")
    gross = gross.replace("]", "")
    gross = gross.replace(",", "")

    if " million" in gross:
        gross = gross.split(" ")
        gross[0] = float(gross[0])
        gross[0] *= 1000000

    if " billion" in gross:
        gross = gross.split(" ")
        gross[0] = float(gross[0])
        gross[0] *= 1000000000

    return int(gross[0])


def parse_year(year):
    """ parse_year parses a raw format of a date to a useful format
        :param year - the year in it's raw format """

    year = year.split("-")
    year = int(year[0])
    return year

# print(scrape_movie("https://en.wikipedia.org/wiki/The_Lego_Movie"))

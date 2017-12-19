from wikiscraper.MovieScraper import scrape_movie
from wikiscraper.ActorScraper import scrape_actor

import json
import logging


class WikiScraper:
    """ a WikiScraper class that scrapes wikipedia in search of actors and movies """

    def scrape_wikipedia(self, url, json_filenumber):
        """ scrapes wikipedia recursively using given url
            :param url - the url to start scraping with
            :param json_filenumber - the filenumber for json file to store the parsed data in """

        actors_count = 0
        movies_count = 0

        actors = []
        movies = []

        actors_urls = []
        movies_urls = []

        logging.basicConfig(filename="./logs/scrape_wikipedia.log")

        first_movie = scrape_movie(url)

        if first_movie is None:
            logging.warning("input url did not lead to anything; try again")
            return None
        else:
            movies_count += 1
            movies.append(first_movie)
            movies_urls.append(first_movie)

            while actors_count < 10 and movies_count < 10:
                if (len(actors_urls) == 0) and (len(movies_urls) == 0):
                    logging.warning("finished parsing all available data")
                    break
                else:
                    while len(actors_urls) != 0:
                        scrape_object = actors_urls.pop(0)
                        movies_count += self.scrape_movies_recursively(scrape_object["movies"], movies, movies_urls)

                    while len(movies_urls) != 0:
                        scrape_object = movies_urls.pop(0)
                        actors_count += self.scrape_actors_recursively(scrape_object["cast"], actors, actors_urls)

            WikiScraper.write_to_json({"Movies":movies}, "./data/movies" + str(json_filenumber))
            WikiScraper.write_to_json({"Actors":actors}, "./data/actors" + str(json_filenumber))

        return [actors_count, movies_count]

    def scrape_actors_recursively(self, obj, obj_list, obj_urls):
        """ scrape actors method scrapes for more actors based on if the data already exists
            :param obj - object to be parsed
            :param obj_list - the list in which to check if the obj already exists
            :param obj_urls - the list of urls to use to recursively scrape """

        count = 0
        parse = None
        for i in obj:
            if not any(j["name"] == i[0] for j in obj_list):
                parse = scrape_actor(i[1])
            if parse is not None:
                obj_list.append(parse)
                obj_urls.append(parse)
                count += 1
            else:
                continue
        return count

    def scrape_movies_recursively(self, obj, obj_list, obj_urls):
        """ scrape actors method scrapes for more movies based on if the data already exists
            :param obj - object to be parsed
            :param obj_list - the list in which to check if the obj already exists
            :param obj_urls - the list of urls to use to recursively scrape """

        count = 0
        parse = None
        for i in obj:
            if not any(j["name"] == i[0] for j in obj_list):
                parse = scrape_movie(i[1])
            if parse is not None:
                obj_list.append(parse)
                obj_urls.append(parse)
                count += 1
            else:
                continue
        return count

    @staticmethod
    def write_to_json(data, filename):
        """ write_to_json converts raw data to json file format
            :param data - the data to be stored as json
            :param filename - the filename for the output json """

        with open(filename + '.json', 'w') as fpA:
            json.dump(data, fpA, sort_keys=True, indent=2)

    @staticmethod
    def read_from_json(filename):
        """ read_from_json converts a json file format into raw data
            :param filename - the filename for the output data """

        with open(filename, 'r') as file:
            return json.load(file)


if __name__ == "__main__":
    wiki_scrape = WikiScraper().scrape_wikipedia("https://en.wikipedia.org/wiki/Elysium_(film)", 0)
    print "actors parsed: " + str(wiki_scrape[0])
    print "movies parsed: " + str(wiki_scrape[1])

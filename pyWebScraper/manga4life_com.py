"""! @brief Defines the Manga Feed class """

################################################################################
# @file bot.py
#
# @brief This file defines class(es) and function(s) for pyWebScraper.
#
# @section Description
# Defines class for MangaFeed
# - clsMangaFeed
#
# @section Libraries/Modules
# - datetime standard library
#    + Access today and date method in datetime class
# - re standard library
#    + Access search method
# - os standard library
#    + Access to exists method in path module
#    + Access to remove method
# - json standard library
#    + Access to loads method
# - yaml open-source library
#    + Access to loads method
#    + Access to YAML Loader "yaml.CLoader"
# - requests open-source library
#    + Access to Session class
# - generic local library
#    + [RO] gConfig
#    + [RW] gMangaFeed
#
# @section NOTE
# - None
#
# @section TODO
# - None
#
# @section Change History
# Example description:
# Version Y-M-D       Author      Change description
# 1.0.0   2022-01-22  Tin Luu     Initial Version
#
# Copyright (c) 2022 Pennyworth Project.  All rights reserved.
################################################################################

# Get shared variable across modules
from pyAbstract import generic
from pyAbstract.generic import DEM

# Import standard library
import re
import json
from os.path import exists
from os import remove

# Import open-source library
import yaml
from requests import Session
from bs4 import BeautifulSoup

# Import custom library
from generated.SECRET_WEBSCRAPER import *
from generated.FILE import *
from pyWebScraper.LITERALS import *
from pyDiagnostic.DTC import *

class clsMangaFeed(Session):
    """! The Discord Bot base class.
    Defines the base class utilized the Discord Bot.
    """

    def __init__(self) -> None:
        """! The Manga Feed class initializer.

        @param  None.
        @return  None.
        """
        # Initialization with base class
        super().__init__()

        try:
            self.feed = []
            # When manga-feed.yml is existed
            if exists(FILE_NOTIFICATION_MANGA):
                # Open manga-feed.yml as standard input stream
                with open(FILE_NOTIFICATION_MANGA, OPEN_PERMISSION_READ) as stream:
                    # Load manga-feed.yml to MangaFeed
                    self.feed = yaml.load(stream, Loader=yaml.CLoader)
                # Remove manga-feed.yml
                remove(FILE_NOTIFICATION_MANGA)

            MANGA4LIFE_LOGIN_PAYLOAD[
                MANGA4LIFE_KEYWORD_EMAILADDRESS
            ] = SECRET_WEBSCRAPER_MANGA4LIFE_EMAILADDRESS
            MANGA4LIFE_LOGIN_PAYLOAD[
                MANGA4LIFE_KEYWORD_PASSWORD
            ] = SECRET_WEBSCRAPER_MANGA4LIFE_PASSWORD
            self._login_payload = MANGA4LIFE_LOGIN_PAYLOAD
            self.logged = False
            DEM.set_event_status(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_INIT)
        except:
            DEM.set_event_status(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_INIT_FAILED)

    def login(self):
        # Get login URL
        _url = MANGA4LIFE_URL_LOGIN
        # Invoke POST request with payload JSON
        request = self.post(_url, json=self._login_payload)
        # Load response of POST request
        result = json.loads(request.text)
        # Check result of response
        self.logged = all(
            [
                result[MANGA4LIFE_LITERAL_SUCCESS],
                bool(result[MANGA4LIFE_LITERAL_VAL] == MANGA4LIFE_LITERAL_OK),
            ]
        )
        if not self.logged:
            DEM.set_event_status(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_LOGIN_FAILED)
        else:
            DEM.set_event_status(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_LOGIN)

    def dump_notification(self):
        if self.feed:
            # Open manga-feed.yml as standard input stream
            with open(FILE_NOTIFICATION_MANGA, OPEN_PERMISSION_WRITE) as stream:
                # Dump manga feed to output file
                yaml.dump(self.feed, stream, default_flow_style=False)

    async def check_feed(self) -> None:
        if not self.logged:
            DEM.set_event_status(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_NOT_LOGGED)
            return

        feed_raw = self._get_feed_data()
        feed_db = list()
        for entry in map(
            self._extract_feed_entry,
            [MANGA4LIFE_URL_READ] * len(feed_raw),
            feed_raw,
        ):
            feed_db.append(entry)

        feed_db.sort()

        if exists(FILE_DATABASE_MANGA):
            with open(FILE_DATABASE_MANGA, OPEN_PERMISSION_READ) as stream:
                feed_db_ori = yaml.load(stream, Loader=yaml.CLoader)
            new_update = [entry for entry in feed_db if entry not in set(feed_db_ori)]
            self.feed = new_update

        with open(FILE_DATABASE_MANGA, OPEN_PERMISSION_WRITE) as stream:
            yaml.dump(feed_db, stream, default_flow_style=False)

    def _extract_feed_entry(self, prefix_url, entry):
        # Get chapter information
        # Chapter information is equal to chapter*10 + 100000
        chapter_no = int(entry[MANGA4LIFE_LITERAL_CHAPTER]) % INT_ONE_HUNDRED_THOUSAND
        chapter_no = (
            int(chapter_no / INT_TEN)
            if (INT_ZERO == chapter_no % INT_TEN)
            else float(chapter_no / FLOAT_TEN)
        )
        # Get IndexName of Series
        indexName = entry[MANGA4LIFE_LITERAL_INDEXNAME]
        dateEntry = entry[MANGA4LIFE_LITERAL_DATE]
        # Get chapter URL
        chapter_url = MANGA4LIFE_FORMAT_CHAPTER_URL.format(
            dateEntry=dateEntry,
            prefix_url=prefix_url,
            indexName=indexName,
            chapter_no=chapter_no,
        )
        return chapter_url

    def _get_feed_data(self):
        url = MANGA4LIFE_URL_FEED
        # Get feed URL
        try:
            # Parse feed response using Beautiful Soup
            soup = BeautifulSoup(self.get(url).content, HTML_PARSER)
            # Get content of feed response
            content = soup.find_all(MANGA4LIFE_LITERAL_SCRIPT)[
                LIST_ELEMENT_INDEX_LAST
            ].string
            # Get vmFeedJSON from script
            vmFeedJSON = re.search(MANGA4LIFE_REGEX_SEARCH, content)
            # Load vmFeedJSON to data local variables
            if not vmFeedJSON is None:
                DEM.set_event_status(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_GET_FEED_SUCCEED)
                return json.loads(str(vmFeedJSON.group(FIRST_GROUP_INDEX)))
            DEM.set_event_status(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_GET_FEED_FAILED)
            return {}
        except:
            DEM.set_event_status(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_GET_FEED_FAILED)
            return {}


################################################################################
# END OF FILE
################################################################################

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
import abc
from datetime import datetime
from os.path import exists

# Import open-source library
import yaml
from requests import Session
from bs4 import BeautifulSoup

from generated.FILE import *
from pyWebScraper.LITERALS import *


class clsProduct(object):
    def __init__(self) -> None:
        self.sale_price = STR_VALUE_DUMMY
        self.name = STR_VALUE_DUMMY


class clsProductSalePriceBase(Session):
    __metaclass__ = abc.ABCMeta

    def __init__(self) -> None:
        super().__init__()
        self.base_url = STR_VALUE_DUMMY
        self.db_name = STR_VALUE_DUMMY
        self.database = []

    @abc.abstractclassmethod
    def _get_product_info(self, product_id: str) -> clsProduct:
        """Method documentation"""
        return clsProduct()

    def load_database(self) -> None:
        if exists(FILE_DATABASE_WISHLIST):
            with open(FILE_DATABASE_WISHLIST, OPEN_PERMISSION_READ) as stream:
                wishlist_database = yaml.load(stream, Loader=yaml.CLoader)
                self.database = wishlist_database[self.db_name]

    def dump_database(self) -> None:
        if exists(FILE_DATABASE_WISHLIST):
            with open(FILE_DATABASE_WISHLIST, OPEN_PERMISSION_READ) as stream:
                wishlist_database = yaml.load(stream, Loader=yaml.CLoader)
                wishlist_database[self.db_name] = self.database
            with open(FILE_DATABASE_WISHLIST, OPEN_PERMISSION_WRITE) as stream:
                yaml.dump(wishlist_database, stream, default_flow_style=False)

    async def check_feed(self) -> None:
        if bool(self.database):
            for product in self.database:
                proObj = self._get_product_info(product[SALEPRICE_KEYWORD_ID])
                now = datetime.now()
                dt_string = now.strftime(SALEPRICE_TIME_FORMAT)
                is_updated = False
                percentage = INT_ONE
                if not SALEPRICE_KEYWORD_PRICE in product:
                    product[SALEPRICE_KEYWORD_PRICE] = []
                    is_updated = True
                if not is_updated:
                    last_price = (
                        list(
                            product[SALEPRICE_KEYWORD_PRICE][
                                LIST_ELEMENT_INDEX_LAST
                            ].values()
                        )
                    )[LIST_ELEMENT_INDEX_FIRST]
                    compare = int(proObj.sale_price) == last_price
                    if not compare:
                        percentage = float(proObj.sale_price) / float(last_price)
                        is_updated = True
                if is_updated:
                    product[SALEPRICE_KEYWORD_NAME] = proObj.name
                    product[SALEPRICE_KEYWORD_PRICE].append(
                        {dt_string: int(proObj.sale_price)}
                    )
                    product[SALEPRICE_KEYWORD_PERCENTAGE] = (
                        str(round(percentage * INT_ONE_HUNDRED, INT_TWO))
                        + CHAR_PERCENTAGE
                    )
                product[SALEPRICE_KEYWORD_UPDATE] = is_updated


class clsGearVN(clsProductSalePriceBase):
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
        self.base_url = GEARVN_URL_BASE
        self.db_name = GEARVN_DATABASE_NAME

    def _get_product_info(self, product_id: str) -> clsProduct:
        request = self.get(self.base_url + GEARVN_PRODUCT_URL_EXT + product_id)
        soup = BeautifulSoup(request.content, HTML_PARSER)
        product = clsProduct()
        sale_price = (
            (soup.find_all(GEARVN_SALEPRICE_ELEMENT, GEARVN_SALEPRICE_PROPERTY))[
                LIST_ELEMENT_INDEX_FIRST
            ]
            .text.lstrip()
            .rstrip()
        )
        sale_price = re.findall(SALEPRICE_REGEX_DIGIT_ONLY, sale_price)
        product.sale_price = EMPTY_STR.join(sale_price)
        product.name = (
            ((soup.find_all(GEARVN_NAME_ELEMENT, GEARVN_NAME_PROPERTY)))[
                LIST_ELEMENT_INDEX_FIRST
            ]
            .text.lstrip()
            .rstrip()
        )
        return product


class clsCellphoneS(clsProductSalePriceBase):
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
        self.base_url = CELLPHONES_URL_BASE
        self.db_name = CELLPHONES_DATABASE_NAME

    def _get_product_info(self, product_id: str) -> clsProduct:
        request = self.get(self.base_url + product_id + CELLPHONES_PRODUCT_SUFFIX)
        soup = BeautifulSoup(request.content, HTML_PARSER)
        product = clsProduct()
        sale_price = (
            (
                soup.find_all(
                    CELLPHONES_SALEPRICE_ELEMENT, CELLPHONES_SALEPRICE_PROPERTY
                )
            )[LIST_ELEMENT_INDEX_FIRST]
            .text.lstrip()
            .rstrip()
        )
        sale_price = re.findall(SALEPRICE_REGEX_DIGIT_ONLY, sale_price)
        product.sale_price = EMPTY_STR.join(sale_price)
        product.name = (
            ((soup.find_all(CELLPHONES_NAME_ELEMENT, CELLPHONES_NAME_PROPERTY)))[
                LIST_ELEMENT_INDEX_FIRST
            ]
            .text.lstrip()
            .rstrip()
        )
        return product


################################################################################
# END OF FILE
################################################################################

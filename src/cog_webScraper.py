"""! @brief Defines the clsCogSlashCommand class """

################################################################################
# @file cog_webScraper.py
#
# @section NOTE
# - clsCogSlashCommand.cog_load: reserved, for action do when loading cog.
# - clsCogSlashCommand.cog_unload: reserved, for action do when unloading cog.
#
# @section TODO
# - None
#
# @section Change History
# Example description:
# Version Y-M-D       Author      Change description
# 1.0.0   2023-02-20  Tin Luu     Initial Version
#
# Copyright (c) 2022 Pennyworth Project.  All rights reserved.
################################################################################

# Get shared variable across modules
#   + [INVOKE] callback.MSG_INJECT
from src.pyAbstract import CALLBACK
from src.pyAbstract.generic import DEM

# Import standard library
from types import SimpleNamespace
import time

# Import open-source library
from discord import app_commands, Interaction
from discord.ext import commands, tasks
from typing import List

# Import custom Library
from generated.DISCORD import *
from generated.DTC import *
from src.pyAbstract.LITERALS import *
from src.pyDiscordBot.LITERALS import *
from src.pyWebScraper import Manga4Life, GearVN, CellphoneS


class clsCogWebScraper(commands.Cog):
    """Discord Bot Cog that scrape the Webs and collect the info

    Functionalities
    ---------------
    + Scheduled task to notify all message in queue
    + Scheduled task to validate delivered messages in home server with Discord
    + /wishlist_update website[GearVN|CellphoneS] action[add|remove] item_id: to add/remove item to wishlist
    + /wishlist action[list|restart]: to list current items or to restart task

    """

    def __init__(self, bot) -> None:
        """Discord Bot Cog that scrape the Webs and collect the info

        Functionalities
        ---------------
        + Scheduled task to notify all message in queue
        + Scheduled task to validate delivered messages in home server with Discord
        + /wishlist_update website[GearVN|CellphoneS] action[add|remove] item_id: to add/remove item to wishlist
        + /wishlist action[list|restart]: to list current items or to restart task

        Args
        ----
        + [IN] bot (discord.commands.Bot): refer to Discord Bot loaded this cog

        Returns/Raises/DTC
        ------------------
        + None

        """

        """ Sequence:
        1. Assign bot of this class to bot loading the cog
        2. Loading input to object variables
        3. Configurating cog list to load cog in on_ready event
        
        """

        # 1. Assign bot of this class to bot loading the cog
        self.bot = bot

        # 2. Start the tasks
        self._MainFunction_Manga4Life_Feed.start()
        self._MainFunction_SalePrice_Feed.start()

        DEM.set_event_status(DEM_EVENT_DISCORD_COG_WEB_SCRAPER_INIT)

    def cog_load(self) -> None:
        """! Program sequence to invoke when loading cog

        Functionalities
        ---------------
        + Creating spiders that crawl the Web
        + Assigning callback function for Injection

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Create spiders that crawl the Web
        2. Load wishlist database
        3. Login Manga4Life
        
        """

        # 1. Create spiderS
        self.spider = SimpleNamespace()
        self.spider.MangaFeed = Manga4Life()
        self.spider.GearVN = GearVN()
        self.spider.CellphoneS = CellphoneS()

        self.spider.CellphoneS.load_database()
        self.spider.GearVN.load_database()

        # 2. Load wishlist database

        # 3. Login Manga4Life
        self.spider.MangaFeed.login()

        DEM.set_event_status(DEM_EVENT_DISCORD_COG_WEB_SCRAPER_COG_LOAD)

    def cog_unload(self) -> None:
        """! Program sequence to invoke when unloading cog

        Functionalities
        ---------------
        + Creating spiders that crawl the Web
        + Assigning callback function for Injection

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Dump remaining notification
        2. Dump data to database
        3. Stop and cancel running tasks
        
        """

        # 1. Dump remaining notification
        self.spider.MangaFeed.dump_notification()

        # 2. Dump data to database
        self.spider.CellphoneS.dump_database()
        self.spider.GearVN.dump_database()

        # 3. Stop and cancel running tasks
        try:
            # Stop tasks
            self._MainFunction_Manga4Life_Feed.stop()
            self._MainFunction_SalePrice_Feed.stop()

        except AttributeError:
            pass

        DEM.set_event_status(DEM_EVENT_DISCORD_COG_WEB_SCRAPER_COG_UNLOAD)

    @tasks.loop(hours=DISCORD_COG_WEBSCRAPER_LOOP_INTERVAL_HOURS_MANGA4LIFE)
    async def _MainFunction_Manga4Life_Feed(self):
        """Task schedule in background and repeat permantly to check feed of Manga4Life

        Functionalities
        ---------------
        + Creating spiders that crawl the Web
        + Assigning callback function for Injection

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Check Manga4Life Feed
        2. If there is new feed, inject it to message queue, then clear the queue
        
        """

        DEM.set_event_status(
            DEM_EVENT_DISCORD_COG_WEB_SCRAPER_MAINFUNCTION_MANGAFEED_CYCLE_START
        )

        # 1. Check Manga4Life Feed
        await self.spider.MangaFeed.check_feed()

        # 2. If there is new feed, inject it to message queue, then clear the queue
        # 2.1. If there is new feed
        if bool(self.spider.MangaFeed.feed):

            # 2.2. Inject new feed to message queue
            for entry in self.spider.MangaFeed.feed:
                await CALLBACK.MSG_INJECT(
                    DISCORD_BOT_CHANNELS[CHANNELS_INDER_MANGAFEED],
                    COG_WEBSCRAPER_MSG_001.format(entry=entry),
                )

            # 2.3. Clear the queuq
            self.spider.MangaFeed.feed.clear()

        ### Log INFO
        DEM.set_event_status(
            DEM_EVENT_DISCORD_COG_WEB_SCRAPER_MAINFUNCTION_MANGAFEED_CYCLE_END
        )

    @_MainFunction_Manga4Life_Feed.before_loop
    async def _MainFunction_Notify_before(self):
        """Program sequece that run before task

        Functionalities
        ---------------
        + Waiting until Manga4Life is logged in

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Wait until manga4life is login
        
        """

        # 1. Wait until manga4life is login
        while not self.spider.MangaFeed.logged:
            # 1.1. Do nothing
            if DEM.lookup(DEM_EVENT_WEBSCRAPER_MANGA4LIFE_LOGIN_FAILED):
                DEM.set_event_status(
                    DEM_EVENT_DISCORD_COG_WEB_SCRAPER_MAINFUNCTION_MANGAFEED_CYCLE_CANCEL
                )
                self._MainFunction_Manga4Life_Feed.stop()
                return

    @tasks.loop(hours=DISCORD_COG_WEBSCRAPER_LOOP_INTERVAL_HOURS_SALEPRICE)
    async def _MainFunction_SalePrice_Feed(self):
        """Task schedule in background and repeat permantly to check new of Wishlist

        Functionalities
        ---------------
        + Waiting until Manga4Life is logged in

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Check feed and compare to last data
        2. Check for updated entries and notify
        
        """

        DEM.set_event_status(
            DEM_EVENT_DISCORD_COG_WEB_SCRAPER_MAINFUNCTION_SALEPRICE_CYCLE_START
        )

        # 1. Check feed and compare to last data
        await self.spider.GearVN.check_feed()
        await self.spider.CellphoneS.check_feed()

        # 2. Check for updated entries and notify
        product_list = list(self.spider.CellphoneS.database) + list(
            self.spider.GearVN.database
        )
        for product in product_list:
            if product[WISHLISTT_PRODUCT_KEYWORD_UPDATE]:
                await CALLBACK.MSG_INJECT(
                    STR_DUMMY,
                    COG_WEBSCRAPER_MSG_002.format(
                        product_name=product[WISHLISTT_PRODUCT_KEYWORD_NAME],
                        product_price=(
                            list(
                                product[WISHLISTT_PRODUCT_KEYWORD_PRICE][
                                    ELEMENT_INDEX_LAST
                                ].values()
                            )
                        )[ELEMENT_INDEX_FIRST],
                        product_percentage=product[
                            WISHLISTT_PRODUCT_KEYWORD_PERCENTAGE
                        ],
                    ),
                )

        # Log DBG
        DEM.set_event_status(
            DEM_EVENT_DISCORD_COG_WEB_SCRAPER_MAINFUNCTION_SALEPRICE_CYCLE_END
        )

    async def _wishlist_update_ws_autocomplete(
        self,
        interaction: Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        """Autocomplete argument 'website' of wishlist_update

        Functionalities
        ---------------
        + Return choice for autocomplete argument 'website'

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Define the choice of slash command argument
        2. Return the choice of slash command argument
        
        """

        # 1. Define the choice of slash command argument

        # 2. Return the choice of slash command argument
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in WISHLIST_WEBSITE
            if current.lower() in choice.lower()
        ]

    async def _wishlist_update_act_autocomplete(
        self,
        interaction: Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        """Autocomplete argument 'action' of wishlist_update

        Functionalities
        ---------------
        + Return choice for autocomplete argument 'website'

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Define the choice of slash command argument
        2. Return the choice of slash command argument
        
        """

        # 1. Define the choice of slash command argument

        # 2. Return the choice of slash command argument
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in WISHLIST_UPDATE_ACTION
            if current.lower() in choice.lower()
        ]

    def _wishlist_update_add(self, website: str, item_id: str) -> str:
        """Add wish item to the list if not existed

        Functionalities
        ---------------
        + Add wish item to the list if not existed

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Check whether wish item is existed in the list
        2. Add item id to list if new and define message to reply
        3. Return reply message

        """

        # 1. Check whether wish item is existed in the list
        spider = [self.spider.GearVN, self.spider.CellphoneS][
            WISHLIST_WEBSITE.index(website)
        ]

        is_new_item = True
        for product in spider.database:
            if product[WISHLISTT_PRODUCT_KEYWORD_ID] == item_id:
                is_new_item = False
                break

        # 2. Add item id to list if new and define message to reply
        if is_new_item:
            spider.database.append({WISHLISTT_PRODUCT_KEYWORD_ID: item_id})
            message = COG_WEBSCRAPER_MSG_003.format(item_id=item_id, website=website)
        else:
            message = COG_WEBSCRAPER_MSG_004.format(item_id=item_id, website=website)

        # 3. Return reply message
        DEM.set_event_status(
            DEM_EVENT_DISCORD_COG_WEB_SCRAPER_COMMAND_WISHLIST_UPDATE_ADD
        )
        return message

    def _wishlist_update_remove(self, website: str, item_id: str):
        """Remove wish item to the list if existed

        Functionalities
        ---------------
        + Remove wish item to the list if existed

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Remove item id to list if new
        2. Define message to reply
        3. Return reply message

        """

        spider = [self.spider.GearVN, self.spider.CellphoneS][
            WISHLIST_WEBSITE.index(website)
        ]

        # 1. Remove item id to list if new
        remove = False
        for product in spider.database:
            if product[WISHLISTT_PRODUCT_KEYWORD_ID] == item_id:
                spider.database.remove(product)
                remove = True

        # 2. Define message to reply
        if not remove:
            message = COG_WEBSCRAPER_MSG_005.format(item_id=item_id, website=website)
        else:
            message = COG_WEBSCRAPER_MSG_006.format(item_id=item_id, website=website)

        # 3. Return reply message
        DEM.set_event_status(
            DEM_EVENT_DISCORD_COG_WEB_SCRAPER_COMMAND_WISHLIST_UPDATE_REMOVE
        )
        return message

    async def _wishlist_act_autocomplete(
        self,
        interaction: Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        """Autocomplete argument 'action' of wishlist

        Functionalities
        ---------------
        + Return choice for autocomplete argument 'website'

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Define the choice of slash command argument
        2. Return the choice of slash command argument
        
        """

        # 1. Define the choice of slash command argument

        # 2. Return the choice of slash command argument
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in WISHLIST_ACTION
            if current.lower() in choice.lower()
        ]

    @app_commands.command()
    @app_commands.describe(
        website=WISHLIST_WEBSITE_DESCRIPTION,
        action=WISHLIST_UPDATE_ACTION_DESCRIPTION,
        item_id=WISHLIST_UPDATE_ITEM_ID_DESCRIPTION,
    )
    @app_commands.autocomplete(website=_wishlist_update_ws_autocomplete)
    @app_commands.autocomplete(action=_wishlist_update_act_autocomplete)
    async def wishlist_update(
        self, interaction: Interaction, website: str, action: str, item_id: str
    ):
        """Update current wishlist

        Functionalities
        ---------------
        + /wishlist_update [GearVN|CellphoneS] add {item_id}: Add item_id to wishlist
        + /wishlist_update [GearVN|CellphoneS] remove {item_id}: Remove item_id to wishlist

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Check whether input website is valid
        2. If action is 'add', proceed with 'add' sequence
        3. If action is 'remove', proceed with 'remove' sequence
        4. Reply to the server

        """

        # 1. Check whether input website is valid
        if not website in WISHLIST_WEBSITE or not action in WISHLIST_UPDATE_ACTION:
            message = COG_WEBSCRAPER_MSG_007
            DEM.set_event_status(
                DEM_EVENT_DISCORD_COG_WEB_SCRAPER_COMMAND_WISHLIST_UPDATE_UNSUPPORTED
            )

        # 2. If action is 'add', proceed with 'add' sequence
        action_sequence = [self._wishlist_update_add, self._wishlist_update_remove]
        message = action_sequence[WISHLIST_WEBSITE.index(website)](website, item_id)

        # 3. Reply to the server
        await interaction.response.send_message(message, ephemeral=False)

    @app_commands.command()
    @app_commands.describe(
        action=WISHLIST_ACTION_DESCRIPTION,
    )
    @app_commands.autocomplete(action=_wishlist_act_autocomplete)
    async def wishlist(self, interaction: Interaction, action: str):
        """Update current wishlist

        Functionalities
        ---------------
        + /wishlist list: List current item_id of wishlist
        + /wishlist restart: Restart scheduled task of check wishlist feed

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. If action is 'list', proceed with 'list' sequence
        2. If action is 'restart', proceed with 'restart' sequence
        3. Reply to the server

        """

        # 1. If action is 'list', proceed with 'list' sequence
        if action == WISHLIST_ACTION[ELEMENT_INDEX_FIRST]:
            message = COG_WEBSCRAPER_MSG_008
            for product in self.spider.GearVN.database:
                message = message + COG_WEBSCRAPER_MSG_009.format(
                    product_id=product[WISHLISTT_PRODUCT_KEYWORD_ID]
                )
            message = message + COG_WEBSCRAPER_MSG_010
            for product in self.spider.CellphoneS.database:
                message = message + COG_WEBSCRAPER_MSG_009.format(
                    product_id=product[WISHLISTT_PRODUCT_KEYWORD_ID]
                )
            DEM.set_event_status(
                DEM_EVENT_DISCORD_COG_WEB_SCRAPER_COMMAND_WISHLIST_LIST
            )

        # 2. If action is 'restart', proceed with 'restart' sequence
        elif action == WISHLIST_ACTION[ELEMENT_INDEX_SECOND]:
            message = COG_WEBSCRAPER_MSG_011
            self._MainFunction_SalePrice_Feed.restart()
            DEM.set_event_status(
                DEM_EVENT_DISCORD_COG_WEB_SCRAPER_COMMAND_WISHLIST_RESTART
            )

        # Check whether input action is valid
        else:
            DEM.set_event_status(
                DEM_EVENT_DISCORD_COG_WEB_SCRAPER_COMMAND_WISHLIST_UNSUPPORTED
            )
            message = COG_WEBSCRAPER_MSG_007

        # 3. Reply to the server
        await interaction.response.send_message(message, ephemeral=False)


################################################################################
# END OF FILE
################################################################################

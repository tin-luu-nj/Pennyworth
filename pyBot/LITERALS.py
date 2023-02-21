"""! @brief Defines the clsCogSlashCommand class """

################################################################################
# @file cog_webScraper.py
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
# 1.0.0   2023-02-20  Tin Luu     Initial Version
#
# Copyright (c) 2022 Pennyworth Project.  All rights reserved.
################################################################################

# Channels list element index
CHANNELS_INDEX_SERVER = 0
CHANNELS_INDER_MANGAFEED = 1

# Message to send to server in pyBot.bot.py
BOT_MSG_001 = f"Alfred is at your service!\n"
BOT_MSG_002 = f"Alfred is offline!\n"

# Message for Log DBG in pyBot.bot.py
BOT_LOG_DBG_001 = "Discord Bot initialized"
BOT_LOG_DBG_002 = "Synced {len_synced} command(s)"
BOT_LOG_DBG_003 = "Discord Bot is ready"
BOT_LOG_DBG_004 = "Discord Bot is cleaning up"
BOT_LOG_DBG_005 = "Discord Bot is closing"
BOT_LOG_DBG_006 = "Discord Bot sent message: {message}"
BOT_LOG_DBG_007 = "Discord Bot running"

# Message for Log INFO in pyBot.bot.py
BOT_LOG_INFO_001 = "{user} is connected to the {guild_name} guild with id: {guild_id}"

# Message to send to server in pyBot.cog_slashcommand.py
COG_SLASHCOMMAND_MSG_001 = (
    "Hi {mention}!\nAlfred is up for {runtime} since {startTime}!\n"
)
COG_SLASHCOMMAND_MSG_002 = "Alfred is shutting down!"

# Message for Log DBG in pyBot.cog_slashcommand.py
COG_SLASHCOMMAND_LOG_INFO_001 = "slashCommand status"

# Message for Log DBG in pyBot.cog_webscraper.py
COG_WEBSCRAPER_MSG_001 = "New chapter release:\n{entry}"
COG_WEBSCRAPER_MSG_002 = "Product Info: {product_name}\nSale Price: VND{product_price}\nPercentage: {product_percentage}"
COG_WEBSCRAPER_MSG_003 = "{item_id} is added to wishlist of {website}.\nProduct Info will be updated in next cycle."
COG_WEBSCRAPER_MSG_004 = "{item_id} is already existed in wishlist of {website}"
COG_WEBSCRAPER_MSG_005 = "{item_id} is not existed in wishlist of {website}."
COG_WEBSCRAPER_MSG_006 = "{item_id} is removed to wishlist of {website}."
COG_WEBSCRAPER_MSG_007 = "Website or Action is not supported"
COG_WEBSCRAPER_MSG_008 = "Wishlist of GearVN contains:"
COG_WEBSCRAPER_MSG_009 = "\n+\t{product_id}"
COG_WEBSCRAPER_MSG_010 = "\n\nWishlist of CellphoneS contains:"
COG_WEBSCRAPER_MSG_011 = "MainFunction WebScraper restart!"

# Message for Log DBG in pyBot.cog_webscraper.py
COG_WEBSCRAPER_LOG_INFO_001 = "Cog of Web Scrapper is initialized!"
COG_WEBSCRAPER_LOG_INFO_002 = "Cog of Web Scrapper is loaded!"
COG_WEBSCRAPER_LOG_INFO_003 = "MainFunction of Manga4Life finished its cycle!"
COG_WEBSCRAPER_LOG_INFO_004 = "MainFunction of SalePrice finished its cycle!"
COG_WEBSCRAPER_LOG_INFO_005 = "Cog of Web Scrapper is unloaded!"
COG_WEBSCRAPER_LOG_INFO_006 = (
    "slashCommand wishlist_update {website} {action} {item_id}"
)
COG_WEBSCRAPER_LOG_INFO_007 = "slashCommand wishlist {action}"

# Keyword for Product dictionary
WISHLISTT_PRODUCT_KEYWORD_ID = "id"
WISHLISTT_PRODUCT_KEYWORD_UPDATE = "update"
WISHLISTT_PRODUCT_KEYWORD_NAME = "name"
WISHLISTT_PRODUCT_KEYWORD_PRICE = "price"
WISHLISTT_PRODUCT_KEYWORD_PERCENTAGE = "percentage"

# List for slash command choices
WISHLIST_WEBSITE = ["GearVN", "CellphoneS"]
WISHLIST_ACTION = ["list", "restart"]
WISHLIST_UPDATE_ACTION = ["add", "remove"]

# Unsupported choice for slash command
WISHLIST_WEBSITE_UNSUPPORTED = "UNSUPPORTED"

# Choice description for slash command
WISHLIST_WEBSITE_DESCRIPTION = (
    "Website of chosen item. Currently supported GearVN and CellphoneS"
)
WISHLIST_UPDATE_ACTION_DESCRIPTION = (
    "Action to do with chosen item. Currently supported: add, remove"
)
WISHLIST_UPDATE_ITEM_ID_DESCRIPTION = "ID of monitored item. None if action is list"
WISHLIST_ACTION_DESCRIPTION = (
    "Action to do with wishlist. Currently supported: list, restart."
)

################################################################################
# END OF FILE
################################################################################

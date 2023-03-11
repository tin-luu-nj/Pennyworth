"""! @brief Defines the DiscordBot class """

################################################################################
# @file bot.py
#
# @section NOTE
# - None
#
# @section TODO
#
# @section Change History
# Example description:
# Version Y-M-D       Author      Change description
# 1.0.0   2022-01-22  Tin Luu     Initial Version
# 1.1.0   2023-02-20  Tin Luu     New Discord module implemented
#
# Copyright (c) 2022 Pennyworth Project.  All rights reserved.
################################################################################

# Get shared variable across modules
from src.pyAbstract.generic import DEM

# Import Standard Library
# nil

# Import open-source Library
from discord.ext import commands
from discord.utils import get as bot_get
from discord import Intents
from discord import Object as dObject

# Import Cogs for Discord Bot
from generated.DISCORD import *
from generated.DTC import *
from generated.SECRET_DISCORD import *
from src.pyAbstract.LITERALS import *
from src.pyDiscordBot.LITERALS import *
from src.pyAbstract import CALLBACK


class clsBot(commands.Bot):
    """Discord Bot Class.

    Functionalities
    ----------------
    + Create scheduled tasks that run in the background
    + Communicate between Alfred bot on Discord with home server

    """

    def __init__(self, cog: list) -> None:
        """Create Discord Bot.

        Functionalities
        ---------------
        + Create scheduled tasks that run in the background
        + Communicate between Alfred bot on Discord with home server

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Specifying the intents used for Discord Bot
        2. Configurating cog list to load cog in on_ready event
        
        """

        # 1. Basic setting for Discord Bot intents
        # refs: https://discordpy.readthedocs.io/en/stable/intents.html
        intents = Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, command_prefix=DISCORD_BOT_COMMAND_PREFIX)

        # 2. Configure Cog for Cog list
        # Each element of the list is a tuple of (cog enable flag, cog)
        self.cog_list = cog

        ### Log DBG
        # DEM.logger.debug(BOT_LOG_DBG_001)
        DEM.set_event_status(DEM_EVENT_DISCORD_BOT_INIT)

    async def on_ready(self) -> None:
        """Program sequence for on_ready event

        Functionalities
        ---------------
        + Getting the guild and text channels that the Bot connected to
        + Notifying server that the bot is active
        + Adding cog to the bot and start the cog
        + Synchronizing slash commands to the Discord Application

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Get the guild that the bot connected to
        2. Get text channels' name in the guild
        3. Send message to Discord Guild to notify Bot is online
        4. Wait until Bot is ready
        5. Add cog to Discord Bot
        6. Sync slash command and copy them to global Discord Bot

        """

        # 1. Get the guild that the bot connected to
        ## 'type: ignore' justification:
        ## these properties exist in self.guild, nut pylint not recognized
        self.guild = bot_get(self.guilds, name=DISCORD_BOT_GUILD)

        # 2. Get text channels' name in the guild
        self.channels = {}
        if self.guild is not None:
            for channel_name in DISCORD_BOT_CHANNELS:
                channel = bot_get(self.guild.text_channels, name=channel_name)
                if channel is not None:
                    self.channels[channel_name] = channel

        # 3. Send message to Discord Guild to notify Bot is online
        await self.channels[DISCORD_BOT_CHANNELS[CHANNELS_INDEX_SERVER]].send(
            BOT_MSG_001
        )

        # 4. Wait until Bot is ready
        await self.wait_until_ready()

        if DISCORD_COG_NOTIFICATION_MAINFUNCTION_NOTIFY:
            CALLBACK.BOT_NOTIFY = self.notify

        # 5. Add cog to Discord Bot
        for (switch, cog) in self.cog_list:
            if switch:
                await self.add_cog(cog(self))

        # FIXME: NOT WORKED
        if not DISCORD_COG_NOTIFICATION_SHUTDOWN_KEYBOARD_SIGNAL_ENABLE:
            self.tree.remove_command(DISCORD_COG_NOTIFICATION_SHUTDOWN_COMMAND)

        # 6. Sync slash command and copy them to global Discord Bot
        synced = await self.tree.sync()
        self.tree.copy_global_to(guild=dObject(id=DISCORD_BOT_GUILDID))
        # DEM.logger.debug(BOT_LOG_DBG_002.format(len_synced=len(synced)))

        ### Log DBG
        DEM.set_event_status(DEM_EVENT_DISCORD_BOT_ON_READY)

    async def cleanup_sequence(self) -> None:
        """Cleanup sequence for for close event

        Functionalities
        ---------------
        + Remove the cog from the running bot

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Get the guild that the bot connected to

        """

        # 1. Remove cog to Discord Bot
        # for (switch, cog) in self.cog_list:
        #     if switch:
        #         await self.remove_cog(cog(self))

        ### Log DBG
        # DEM.logger.debug(BOT_LOG_DBG_004)
        DEM.set_event_status(DEM_EVENT_DISCORD_BOT_CLEANUP)

    async def close(self) -> None:
        """Close the running bot

        Functionalities
        ---------------
        + Cleanup before closing
        + Notifying server that the bot is deactive

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Cleanup sequence before closing
        2. Send message to Discord Guild to notify Bot is offline
        3. Close class instance

        """

        # 1. Cleanup sequence before closing
        await self.cleanup_sequence()

        # 2. Send message to Discord Guild to notify Bot is offline
        if bool(self.channels[DISCORD_BOT_CHANNELS[CHANNELS_INDEX_SERVER]]):
            await self.channels[DISCORD_BOT_CHANNELS[CHANNELS_INDEX_SERVER]].send(
                BOT_MSG_002
            )

        ### Log DBG
        DEM.set_event_status(DEM_EVENT_DISCORD_BOT_CLOSE)

        # 3. Close class instance
        try:
            await super().close()
        except:
            pass

    async def notify(self, channel: str, message: str) -> None:
        """! Send text message to Discord channel

        Functionalities
        ---------------
        + Sending message to Discord

        Args
        ----
        + [IN] channel (str): Discord Text Channel to send message
        + [IN] message (str): Message to send

        Returns/Raises
        --------------
        + None

        DTC
        ---
        + DEM_EVENT_STATUS_DISCORD_BOT_NOTIFY: DTC for message sending failure
        """

        """ Sequence:
        1. Send Message to Channel
        2. If sending in 1. fails, set event status
        """

        # 1. Send Message to Channel
        try:
            await self.channels[channel].send(message)
            ### Log DBG
            # DEM.logger.debug(BOT_LOG_DBG_006.format(message=message))
            DEM.set_event_status(DEM_EVENT_DISCORD_BOT_NOTIFY)

        # 2. If sending in 1. fails, set event status
        except:
            DEM.set_event_status(DEM_EVENT_DISCORD_BOT_NOTIFY_FAILED)

    def run_bot(self):
        """! Start the Discord bot

        Functionalities
        ---------------
        + Run the bot with secret token

        Args/Returns/Raises
        -------------------
        + None

        DTC
        ---
        + DEM_EVENT_STATUS_DISCORD_BOT_RUN_FAILED: DTC for message sending failure
        """

        """ Sequence:
        1. Start the Discord bot
        2. If sending in 1. fails, set event status
        """

        # 1. Start the Discord bot
        try:
            self.run(SECRET_DISCORD_BOT_TOKEN)

        # 2. If running in 1. fails, set event status
        except:
            DEM.set_event_status(DEM_EVENT_DISCORD_BOT_RUN_FAILED)


################################################################################
# END OF FILE
################################################################################

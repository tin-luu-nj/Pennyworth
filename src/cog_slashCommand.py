"""! @brief Defines the clsCogSlashCommand class """

################################################################################
# @file cog_slashCommand.py
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
## [RO] generic.startTime: start time of Application
import os
from src.pyAbstract import generic
from src.pyAbstract.generic import DEM

# Import Standard Library
## datetime.now():get current timestamp
from datetime import datetime

# Import open-source Library
from discord import app_commands, Interaction
from discord.ext import commands

# Import custom Library
from generated.DISCORD import *
from generated.DTC import *

from src.pyAbstract.LITERALS import *
from src.pyDiscordBot.LITERALS import *


class clsCogSlashCommand(commands.Cog):
    """Discord Bot Cog that manage the basic slash commands

    Functionalities
    ---------------
    + /status: Return status, runtime and start time of the Discord Bot
    + /shutdown: Shutdown the Discord Bot

    """

    def __init__(self, bot: commands.Bot) -> None:
        """Discord Bot Cog that manage the basic slash commands

        Functionalities
        ---------------
        + /status: Return status, runtime and start time of the Discord Bot
        + /shutdown: Shutdown the Discord Bot

        Args
        ----
        + [IN] bot [:class:`discord.commands.Bot`]: refer to Discord Bot loaded this cog

        Returns/Raises/DTC
        ------------------
        + None

        """

        """ Sequence:
        1. Assign bot of this class to bot loading the cog
        
        """

        # 1. Assign bot of this class to bot loading the cog
        self.bot = bot
        DEM.set_event_status(DEM_EVENT_DISCORD_COG_BASIC_COMMAND_INIT)

    def cog_load(self):
        """! Program sequence to invoke when loading cog

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        ### Reservation for loading sequence
        DEM.set_event_status(DEM_EVENT_DISCORD_COG_BASIC_COMMAND_COG_LOAD)

    def cog_unload(self):
        """! Program sequence to invoke when unloading cog

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        ### Reservation for unloading sequence
        DEM.set_event_status(DEM_EVENT_DISCORD_COG_BASIC_COMMAND_COG_UNLOAD)

    @app_commands.command()
    async def status(self, interaction: Interaction):
        """! Return status, runtime and start time of the Discord Bot

        Args
        ----
        + [IN] interaction [:class:`Interaction`]: default input parameter of Interaction

        Returns/Raises/DTC
        ------------------
        + None

        """

        """ Sequence:
        1. Calculate runtime of Discord Bot
        2. Send message of status, runtime and start time of the Discord Bot
        
        """

        # 1. Calculate runtime of Discord Bot
        runtime = datetime.now() - generic.startTime

        # 2. Send message of status, runtime and start time of the Discord Bot
        await interaction.response.send_message(
            COG_SLASHCOMMAND_MSG_001.format(
                mention=interaction.user.mention,
                runtime=runtime,
                startTime=generic.startTime,
            ),
            ephemeral=False,
        )

        ### Log INFO
        DEM.set_event_status(DEM_EVENT_DISCORD_COG_BASIC_COMMAND_STATUS)

    @app_commands.command(name=DISCORD_COG_NOTIFICATION_SHUTDOWN_COMMAND)
    @commands.is_owner()
    async def shutdown(self, interaction: Interaction):
        """! Shutdown the Discord Bot

        Args
        ----
        + [IN] interaction [:class:`Interaction`]: default input parameter of Interaction

        Returns/Raises/DTC
        ------------------
        + None

        """

        """ Sequence:
        1. Notify that Alfred shutdown and close the Discord Bot        
        
        """

        # 1. Notify that Alfred shutdown and close the Discord Bot
        await interaction.response.send_message(
            COG_SLASHCOMMAND_MSG_002, ephemeral=False
        )
        DEM.set_event_status(DEM_EVENT_DISCORD_COG_NOTIFICATION_SHUTDOWN_SIGNAL)

    @app_commands.command(name=DISCORD_COG_NOTIFICATION_RESTART_COMMAND)
    @commands.is_owner()
    async def restart_bot(self, interaction: Interaction):
        """! Shutdown the Discord Bot

        Args
        ----
        + [IN] interaction [:class:`Interaction`]: default input parameter of Interaction

        Returns/Raises/DTC
        ------------------
        + None

        """

        """ Sequence:
        1. Notify that Alfred shutdown and close the Discord Bot        
        
        """

        # 1. Notify that Alfred shutdown and close the Discord Bot
        await interaction.response.send_message(
            COG_SLASHCOMMAND_MSG_003, ephemeral=False
        )
        DEM.set_event_status(DEM_EVENT_AUTOUPDATE_APPLICATION_RESTART_REQUIRED)
        DEM.set_event_status(DEM_EVENT_DISCORD_COG_NOTIFICATION_SHUTDOWN_SIGNAL)


################################################################################
# END OF FILE
################################################################################

"""! @brief Defines the DiscordBot class """

################################################################################
# @file cog_notification.py
#
# @section NOTE
# 1. Interval for each loop is pre-defined.
#
# @section TODO
# 1. Interval for each loop is configured in Alfred.yml
#
# @section Change History
# Example description:
# Version Y-M-D       Author      Change description
# 1.0.0   2023-02-21  Tin Luu     Initial Version
#
# Copyright (c) 2022 Pennyworth Project.  All rights reserved.
################################################################################

# Get shared variable across modules
from src.pyAbstract import CALLBACK, generic
from src.pyAbstract.generic import DEM

# Import Standard Library
# nil

# Import open-source Library
import keyboard
from discord import Message
from discord.ext import commands, tasks

# Import custom Library
from generated.DTC import *
from generated.DISCORD import *
from src.pyAbstract.LITERALS import *
from src.pyAutoUpdate import check_for_update, update
from src.pyDiscordBot.LITERALS import *
from src.pyNotification import notificationManager, notificaition_pushover


class clsCogNotification(commands.Cog):
    """Discord Bot Cog that manage the notification from home server

    Functionalities
    ---------------
    + Recording all messages that bot sent
    + Scheduled task to check whether all waiting message are delivered
    + Scheduled task to notify all message in queue
    + Scheduled task to validate delivered messages in home server with Discord
    + Scheduled task to check Shutdown flag and close bot

    """

    def __init__(self, bot: commands.Bot) -> None:
        """Discord Bot Cog that manage the notification from home server

        Functionalities
        ---------------
        + Recording all messages that bot sent
        + Scheduled task to check whether all waiting message are delivered
        + Scheduled task to notify all message in queue
        + Scheduled task to validate delivered messages in home server with Discord
        + Scheduled task to check Shutdown flag and close bot

        Args
        ----
        +[IN] bot (discord.commands.Bot): refer to Discord Bot loaded this cog

        Returns/Raises/DTC
        ------------------
        + None

        """

        """ Sequence:
        1. Assign bot of this class to bot loading the cog
        2. Start the scheduled tasks
        
        """

        # 1. Assign bot of this class to bot loading the cog
        self.bot: commands.Bot = bot

        # 2. Start the scheduled tasks
        self._MainFunction_Check.start()
        self._MainFunction_Notify.start()
        self._MainFunction_Validate.start()
        self._MainFunction_Shutdown.start()
        DEM.set_event_status(DEM_EVENT_DISCORD_COG_NOTIFICATION_INIT)

    def cog_load(self) -> None:
        """! Program sequence to invoke when loading cog

        Functionalities
        ---------------
        + Creating instance for Notification Manager
        + Assigning callback function for Injection

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Initilize Notification Manager
        2. Assign callback function for message injection
        
        """

        # 1. Initilize Notification Manager
        self.notification_manager = notificationManager()

        # 2. Assign callback function for message injection
        CALLBACK.MSG_INJECT = self.notification_manager.inject
        CALLBACK.BOT_DELIVERED_APPEND = self.notification_manager.delivered_append
        if not DISCORD_COG_NOTIFICATION_MAINFUNCTION_NOTIFY:
            CALLBACK.BOT_NOTIFY = notificaition_pushover

        DEM.set_event_status(DEM_EVENT_DISCORD_COG_NOTIFICATION_COG_LOAD)

    def cog_unload(self) -> None:
        """! Program sequence to invoke when unloading cog

        Functionalities
        ---------------
        + None

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Initilize Notification Manager
        2. Assign callback function for message injection
        
        """
        DEM.set_event_status(DEM_EVENT_DISCORD_COG_NOTIFICATION_COG_UNLOAD)

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Task triggered with message event

        Functionalities
        ---------------
        + Recording all messages that bot sent

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Listen to every message sent by the Bot and record it in delivered list
        
        """

        # 1. Listen to every message sent by the Bot and record it in delivered list
        bot_id = DISCORD_BOT_ID
        if bot_id == message.author.id:
            CALLBACK.BOT_DELIVERED_APPEND(message.content)
            DEM.set_event_status(DEM_EVENT_DISCORD_COG_NOTIFICATION_ON_MESSAGE)

    @tasks.loop(seconds=DISCORD_COG_NOTIFICATION_LOOP_INTERVAL_SECONDS_CHECK)
    async def _MainFunction_Check(self):
        """Task schedule in background and repeat permantly to check sending message

        Functionalities
        ---------------
        + Scheduled task to check whether all waiting message are delivered

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Invoke Check function of Notification Manager
        
        """

        # 1. Invoke Check function of Notification manager
        await self.notification_manager.MainFunction_Check()

    @tasks.loop(seconds=DISCORD_COG_NOTIFICATION_LOOP_INTERVAL_SECONDS_NOTIFY)
    async def _MainFunction_Notify(self):
        """! Task schedule in background and repeat permantly to send message periodcally

        Functionalities
        ---------------
        + Scheduled task to notify all message in queue

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Invoke Notify function of Notification manager
        
        """

        # 1. Invoke Notify function of Notification manager
        await self.notification_manager.MainFunction_Notify()

    @tasks.loop(seconds=DISCORD_COG_NOTIFICATION_LOOP_INTERVAL_SECONDS_VALIDATE)
    async def _MainFunction_Validate(self):
        """! Task schedule in background and repeat permantly to Validate sent message

        Functionalities
        ---------------
        + Scheduled task to validate delivered messages in home server with Discord

        Args/Returns/Raises/DTC
        -----------------------
        + None

        """

        """ Sequence:
        1. Invoke Validate function of Notification manager
        
        """

        # Invoke Validate function of Notification manager
        await self.notification_manager.MainFunction_Validate()

    @tasks.loop(seconds=DISCORD_COG_NOTIFICATION_LOOP_INTERVAL_SECONDS_SHUTDOWN)
    async def _MainFunction_Shutdown(self):
        """! Task schedule in background and repeat permantly to check Shutdown signal

        Functionalities:
        + Scheduled task to check Shutdown flag and close bot

        Args/Returns/Raises/DTC:
        + None

        """

        """ Sequence:
        1. When press 'q' on keyboard, program shutdown
        2. When receive shutdown command from server, program shutdown

        """

        # 1. When press 'q' on keyboard, program shutdown
        if DISCORD_COG_NOTIFICATION_SHUTDOWN_KEYBOARD_SIGNAL_ENABLE:
            if keyboard.is_pressed(
                DISCORD_COG_NOTIFICATION_SHUTDOWN_KEYBOARD_SIGNAL_PRESS
            ):
                DEM.set_event_status(DEM_EVENT_DISCORD_COG_NOTIFICATION_SHUTDOWN_SIGNAL)

        # 2. When receive shutdown command from server, program shutdown
        if DEM.lookup(DEM_EVENT_DISCORD_COG_NOTIFICATION_SHUTDOWN_SIGNAL):
            self._MainFunction_Shutdown.stop()
            await self.bot.close()

    @tasks.loop(seconds=DISCORD_COG_NOTIFICATION_LOOP_INTERVAL_SECONDS_UPDATE)
    async def _MainFunction_UpdateCheck(self):
        """! Task schedule in background and repeat permantly

        Functionalities:
        + Scheduled task

        Args/Returns/Raises/DTC:
        + None

        """

        """ Sequence:

        """

        check_for_update()
        if DEM.cleanup(DEM_EVENT_AUTOUPDATE_NEW_VERSION_AVAILABLE):
            update()
            DEM.set_event_status(DEM_EVENT_AUTOUPDATE_APPLICATION_RESTART_REQUIRED)
            DEM.set_event_status(DEM_EVENT_DISCORD_COG_NOTIFICATION_SHUTDOWN_SIGNAL)


################################################################################
# END OF FILE
################################################################################

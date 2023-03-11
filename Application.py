"""! @brief Application """

################################################################################
# @file App.py
#
# @brief Application.
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

# Import statndard library
import sys, os

# Set traceback limit to 0
sys.tracebacklimit = 0

# Global Variable Initialization
from src.pyAbstract.generic import DEM
from generated.DISCORD import *
from generated.DTC import *

# Import local library
from src.pyDiscordBot import DiscordBot

# Main Function
from src import cogNotification, cogWebScraper, cogSlashCommand


def main() -> None:
    """! Main Method.

    @param  None.
    @return  None.
    """
    print("[INFO] Current version: 1.0.0")
    try:
        # Declare object
        Alfred = DiscordBot(
            [
                (DISCORD_COG_NOTIFICATION_ENABLE, cogNotification),
                (DISCORD_COG_WEBSCRAPER_ENABLE, cogWebScraper),
                (DISCORD_COG_BASICSLASHCOMMAND_ENABLE, cogSlashCommand),
            ]
        )

        # Start Alfred service
        # ALWAYS INVOKE AT THE END OF PROGRAM
        # ALL CALLS AFTER ITS INVOCATION ARE BLOCKED.
        Alfred.run_bot()
    # Catch Keyboard Interrupt
    finally:
        DEM.dump_DTC()


# Execution of script
if __name__ == "__main__":
    main()
    if DEM.cleanup(DEM_EVENT_AUTOUPDATE_APPLICATION_RESTART_REQUIRED):
        DEM.cleanup(DEM_EVENT_DISCORD_COG_NOTIFICATION_SHUTDOWN_SIGNAL)
        os.execv(sys.executable, ["python"] + sys.argv)

################################################################################
# END OF FILE
################################################################################

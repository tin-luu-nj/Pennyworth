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
import sys

# Set traceback limit to 0
# sys.tracebacklimit = 0

# Global Variable Initialization
from generated.DISCORD import *
from pyAbstract import CALLBACK
from pyAbstract.generic import DEM

# Import local library
from pyBot import DiscordBot
from pyPushover import notiPush

# Declare object
Alfred = DiscordBot()
if DISCORD_COG_NOTIFICATION_MAINFUNCTION_NOTIFY:
    CALLBACK.BOT_NOTIFY = Alfred.notify
else:
    CALLBACK.BOT_NOTIFY = notiPush
# Main Function


def main() -> None:
    """! Main Method.

    @param  None.
    @return  None.
    """

    try:
        # Start Alfred service
        # ALWAYS INVOKE AT THE END OF PROGRAM
        # ALL CALLS AFTER ITS INVOCATION ARE BLOCKED.
        Alfred.run_bot()
    # Catch Keyboard Interrupt
    finally:
        print("[INF] Closing Loop")

# Execution of script
if __name__ == "__main__":
    try:
        main()
    except RuntimeError:
        pass
    finally:
        DEM.dump_DTC()

################################################################################
# END OF FILE
################################################################################

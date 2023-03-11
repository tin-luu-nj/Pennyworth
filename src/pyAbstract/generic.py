"""! @brief Defines the global variables """

################################################################################
# @file generic.py
#
# @brief This file defines global variables used in whole package.
#
# @section Description
# Defines global variables used in whole package
#
# @section Libraries/Modules
# - asyncio standard library
#    + Access Lock method
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
from src.pyDiagnostic import Diagnostic

# Import standard library
import ctypes, os
from datetime import datetime

try:
    IS_ADMIN = os.getuid() == 0  # type: ignore
except AttributeError:
    IS_ADMIN = ctypes.windll.shell32.IsUserAnAdmin() != 0

# Status of Discord Bot
startTime = datetime.now()

DEM_config = None
DEM = Diagnostic(DEM_config)

dummyHandler = lambda *arg, **kwargs: print("[DBG] DUMMY HANDLER")

# Function Dictionay
dict_function = {"cmdAnyDesk": dummyHandler}

################################################################################
# END OF FILE
################################################################################

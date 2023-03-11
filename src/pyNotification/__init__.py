"""! @brief Defines the pyNotificationManager class """

################################################################################
# @file __init__.py
#
# @brief This file defines class(es) and method(s) for pyNotificationManager.
#
# @section Description
# Defines class for pyNotificatioManager
# - loopNotificationCheck
# - notificationInject
# - notificationCleanup
#
# @section Libraries/Modules
# - None
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

from .manager import clsNotificationManager as notificationManager
from .pushover import notificaition_pushover

################################################################################
# END OF FILE
################################################################################

from datetime import datetime
import logging
from typing import Literal

from generated.FILE import *
from generated.DIAGNOSTIC import *
from pyAbstract.LITERALS import *
from pyDiagnostic.LITERALS import *


class clsDiagnostic(object):
    def __init__(self, config) -> None:
        self.events = []
        if (
            DIAGNOSTIC_LOGGING_HANDLER_STREAM_ENABLE
            or DIAGNOSTIC_LOGGING_HANDLER_FILE_ENABLE
        ):
            self.logger = logging.getLogger(__name__)

        # Add handlers to the logger
        if DIAGNOSTIC_LOGGING_HANDLER_STREAM_ENABLE:
            self.logger.addHandler(self._create_stream_handler())
        if DIAGNOSTIC_LOGGING_HANDLER_FILE_ENABLE:
            self.logger.addHandler(self._create_file_handler())

        # Set basic level for Logger
        if (
            DIAGNOSTIC_LOGGING_HANDLER_STREAM_ENABLE
            or DIAGNOSTIC_LOGGING_HANDLER_FILE_ENABLE
        ):
            self.logger.setLevel(logging.DEBUG)

    def _create_stream_handler(self) -> logging.StreamHandler:
        # Create handlers
        c_handler = logging.StreamHandler()
        # Create formatters and add it to handlers
        c_format = logging.Formatter("%(relativeCreated)s\t%(levelname)s\t%(message)s")
        c_handler.setFormatter(c_format)
        return c_handler

    def _create_file_handler(self) -> logging.FileHandler:
        # Create handlers
        f_handler = logging.FileHandler(FILE_LOG)
        # Create formatters and add it to handlers
        f_format = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
        f_handler.setFormatter(f_format)
        return f_handler

    def clearDTC(self) -> None:
        self.events.clear()

    def set_event_status(self, event: tuple[int, int, int, str]):
        self._logging(event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX])(
            event[DEM_EVENT_TUPLE_NAME_INDEX]
        )

        if (
            event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX]
            >= LOGGING_LEVEL_LIST[LOG_LEVEL_KEYWORD.index(DIAGNOSTIC_DTC_LEVEL)]
        ):
            self.events.append(
                (
                    str(datetime.now()),
                    event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX],
                    event[DEM_EVENT_TUPLE_ID_INDEX],
                    event[DEM_EVENT_TUPLE_STATUS_INDEX],
                )
            )

    def _logging(self, log_level):
        logging_function = [
            self.logger.critical,
            self.logger.error,
            self.logger.warning,
            self.logger.info,
            self.logger.debug,
        ]

        return logging_function[LOGGING_LEVEL_LIST.index(log_level)]

    def lookup(self, event: tuple[int, int, int, str]):
        for entry in self.events:
            if (
                event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX],
                event[DEM_EVENT_TUPLE_ID_INDEX],
                event[DEM_EVENT_TUPLE_STATUS_INDEX],
            ) == entry[1:]:
                return True
        return False

    def dump_DTC(self):
        if DIAGNOSTIC_DTC_LOG:
            with open(FILE_DTC, OPEN_PERMISSION_WRITE) as stream:
                for entry in self.events:
                    stream.write(f"{entry}\n")

    @property
    def last_event(self):
        if len(self.events) > LEN_ZERO:
            return self.events[LIST_ELEMENT_INDEX_LAST]
        else:
            return ()

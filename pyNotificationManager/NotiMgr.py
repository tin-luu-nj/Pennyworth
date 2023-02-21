import asyncio
import yaml

from generated.DISCORD import *
from pyAbstract import CALLBACK
from pyAbstract.LITERALS import *
from pyAbstract.generic import DEM

class _clsAsyncLock(object):
    def __init__(self) -> None:
        self.deliver = asyncio.Lock()
        self.inject = asyncio.Lock()


class clsNotiMgr(object):
    def __init__(self) -> None:
        self.waiting = {}
        self.delivering = {}
        self.delivered = []
        self.lock = _clsAsyncLock()

    async def MainFunction_Check(self) -> None:
        if self.delivering:
            async with self.lock.deliver:
                is_all_delivered = True
                noti = self.delivering
                for channel in noti:
                    if noti[channel]:
                        is_all_delivered = False
                        break
                if is_all_delivered:
                    self.delivering = {}

        if all([(not self.delivering), bool(self.waiting)]):
            async with self.lock.deliver:
                self.delivering = dict(self.waiting)
                self.waiting = {}

    async def MainFunction_Notify(self):
        if bool(self.delivering):
            async with self.lock.deliver:
                for channel, message in (
                    (channel, message)
                    for channel in self.delivering
                    for message in self.delivering[channel]
                ):
                    await CALLBACK.BOT_NOTIFY(channel, message)


    async def MainFunction_Validate(self):
        if bool(self.delivered):
            async with self.lock.deliver:
                for channel in self.delivering:
                    common = list(
                        set(self.delivering[channel]).intersection(self.delivered)
                    )
                    self.delivering[channel] = list(
                        set(self.delivering[channel]) ^ set(common)
                    )
                    self.delivered.clear()

    async def inject(self, channel: str, message: str):
        async with self.lock.inject:
            noti = self.waiting
            if not channel in noti:
                noti[channel] = []
            noti[channel].append(message)

    def delivered_append(self, message):
        self.delivered.append(message)
        with open("./notification/delivered.yml", "a") as stream:
            # Dump remaining message to output file
            if bool(self.delivered):
                for line in self.delivered:
                    stream.write("{}\n".format(line))

    def cleanup(self):
        self._remaining_cleanup(self._get_remaining())

    def _remaining_cleanup(self, remaining: dict):
        waiting = self.waiting
        if waiting:
            for channel in waiting:
                if remaining[channel]:
                    remaining[channel].append(message for message in waiting[channel])
                else:
                    remaining[channel].clear()
        if remaining:
            # Open leftover.yml as standard input stream
            with open("./notification/leftover.yml", "w") as stream:
                # Dump remaining message to output file
                yaml.dump(remaining, stream, default_flow_style=False)

    def _get_remaining(self) -> dict:
        if self.delivered:
            notification = self.delivering
            for channel in notification:
                common = list(set(notification[channel]).intersection(self.delivered))
                notification[channel] = list(set(notification[channel]) ^ set(common))
                self.delivered.clear()
            return dict(notification)
        else:
            return {}

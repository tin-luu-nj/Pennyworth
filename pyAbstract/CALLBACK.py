def dummyFunction(*arg, **kwargs):
    print("[DBG] DUMMY HANDLER")


async def dummyCoroutine(*arg, **kwargs):
    print("[DBG] DUMMY HANDLER")


MSG_INJECT = dummyCoroutine
BOT_NOTIFY = dummyCoroutine
BOT_DELIVERED_APPEND = dummyFunction
import http.client, urllib
from pyAbstract.generic import DEM
from pyAbstract import CALLBACK
from generated.PUSHOVER import *
from generated.SECRET_PUSHOVER import *
from pyDiagnostic.DTC import *

async def notiPush(channel, message):
    try:
        conn = http.client.HTTPSConnection(PUSHOVER_REQUEST_HTTP)
    except:
        DEM.set_event_status(DEM_EVENT_PUSHOVER_HTTPS_CONNECTION_FAILED)
        return

    try:
        conn.request(
            PUSHOVER_REQUEST_METHOD,
            PUSHOVER_REQUEST_API,
            urllib.parse.urlencode(  # type: ignore
                {
                    "token": SECRET_PUSHOVER_BODY_TOKEN,
                    "user": SECRET_PUSHOVER_BODY_USER,
                    "message": message,
                }
            ),
            {"Content-type": PUSHOVER_REQUEST_CONTENT},
        )
    except:
        DEM.set_event_status(DEM_EVENT_PUSHOVER_REQUEST_FAILED)
        return
    
    try:
        conn.getresponse()
        DEM.set_event_status(DEM_EVENT_PUSHOVER_SUCCEED)
        CALLBACK.BOT_DELIVERED_APPEND(message)
    except:
        DEM.set_event_status(DEM_EVENT_PUSHOVER_GET_RESPONSE_FAILED)
        return


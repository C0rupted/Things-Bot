import time
import aiohttp
import datetime

def timetext(name):
    """ Timestamp, but in text form """
    return f"{name}_{int(time.time())}.txt"

def date(target, clock: bool = True, seconds: bool = False, ago: bool = False, only_ago: bool = False):
    if isinstance(target, int) or isinstance(target, float):
        target = datetime.utcfromtimestamp(target)

    unix = int(time.mktime(target.timetuple()))
    timestamp = f"<t:{unix}:{'f' if clock else 'D'}>"
    if ago:
        timestamp += f" (<t:{unix}:R>)"
    if only_ago:
        timestamp = f"<t:{unix}:R>"
    return timestamp


async def api_call(call_uri):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{call_uri}") as response:
            response = await response.json()
            return response
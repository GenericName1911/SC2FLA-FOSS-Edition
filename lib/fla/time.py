from datetime import datetime
from time import gmtime

def GetTime() -> datetime:
    gmt = gmtime()

    return datetime(gmt.tm_year, gmt.tm_mon, gmt.tm_mday, gmt.tm_hour, gmt.tm_min, gmt.tm_sec)
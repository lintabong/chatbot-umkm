from datetime import datetime

def now_timestamp():
    return int(datetime.utcnow().timestamp()*1000)

def now():
    return datetime.utcnow()

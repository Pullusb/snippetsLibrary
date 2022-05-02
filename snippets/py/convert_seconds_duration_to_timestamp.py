## convert a duration time in seconds to human readable format

sec = 20951

# -- using datetime
import datetime
res = datetime.timedelta(seconds=sec)
print(res)
# >>> 5:49:11


# -- using time module
import time
ty_res = time.gmtime(sec)
res = time.strftime("%H:%M:%S", ty_res)
print(res)
# >>> 05:49:11


# -- to hour / minute
def conversion(sec):
   sec_value = sec % (24 * 3600)
   hour_value = sec_value // 3600
   # print("hour(s):", hour_value)
   
   sec_value %= 3600
   min = sec_value // 60
   sec_value %= 60
   # print("Remaining minutes:", min)
   return f'{hour_value}h {min}'
    
res = conversion(sec)
print(res)
# >>> 5h 49min


# -- more complete
TIME_DURATION_UNITS = (
    ('week', 60*60*24*7),
    ('day', 60*60*24),
    ('hour', 60*60),
    ('min', 60),
    ('sec', 1)
)

def human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

res = human_time_duration(sec)
print(res)
# >>> 5 hours, 49 mins, 11 secs

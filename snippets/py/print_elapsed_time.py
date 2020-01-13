import time, datetime
print('Starting', datetime.datetime.now())# print full current date
start_time = time.time()# get start time

# Do stuff

elapsed_time = time.time() - start_time# seconds
full_time = str(datetime.timedelta(seconds=elapsed_time))# hh:mm:ss format

print("elapsed time", elapsed_time)
print(full_time)
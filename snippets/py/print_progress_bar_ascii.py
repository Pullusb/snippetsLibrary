# ASCII progress bar printing
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '=', fill_empty=' '):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    From here:    
    https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + fill_empty * (length - filledLength)
    return '{} |{}| {}/{}{}'.format(prefix, bar, iteration,total, suffix)

# exemple to print on same line in console
from time import sleep
for i in range(0,101):
    sleep(0.01)
    print(print_progress_bar(i, 100, fill='-',length=15), end='\r', flush=True)#flush might not be necessary...
print()#insert a newline for next prints
def transfer_value(value, old_min, old_max, new_min, new_max):
    '''map a value from a range to another (transfer/translate value)'''
    return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

def transfer_value_bis(value, old_min, old_max, new_min, new_max):
    '''detailed transfer value from a range to another'''
    old_range = (old_max - old_min)  
    new_range = (new_max - new_min)  
    new_value = (((value - old_min) * new_range) / old_range) + new_min
    return new_value

transfer_value(${1:value}, ${2:old_min}, ${3:old_max}, ${4:new_min}, ${5:new_max})

#oneliner
new_value = (((${1:value} - ${2:old_min}) * (${5:new_max} - ${4:new_min})) / (${3:old_max} - ${2:old_min})) + ${4:new_min}

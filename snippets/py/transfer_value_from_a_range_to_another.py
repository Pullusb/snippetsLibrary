def transfer_value(Value, OldMin, OldMax, NewMin, NewMax):
    '''map a value from a range to another (transfer/translate value)'''
    return (((Value - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def transfer_value_bis(Value, OldMin, OldMax, NewMin, NewMax):
    '''detailed transfer value from a range to another'''
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((Value - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue

transfer_value(${1:Value}, ${2:OldMin}, ${3:OldMax}, ${4:NewMin}, ${5:NewMax})

#oneliner
NewValue = (((${1:Value} - ${2:OldMin}) * (${5:NewMax} - ${4:NewMin})) / (${3:OldMax} - ${2:OldMin})) + ${4:NewMin}

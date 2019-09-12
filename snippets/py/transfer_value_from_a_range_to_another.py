#map a value from a range to another (transfer/translate value)
#oneliner
NewValue = (((${1:Value} - ${2:OldMin}) * (${5:NewMax} - ${4:NewMin})) / (${3:OldMax} - ${2:OldMin})) + ${4:NewMin}

#detailed
OldRange = (${3:OldMax} - ${2:OldMin})  
NewRange = (${5:NewMax} - ${4:NewMin})  
NewValue = (((${1:Value} - ${2:OldMin}) * NewRange) / OldRange) + ${4:NewMin}
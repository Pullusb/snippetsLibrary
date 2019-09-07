import json
from os.path import join
def jsondump(dictodump, outFilePath):
    '''Save dic as json file at given file path'''
    outfile = open(outFilePath, "w")
    outfile.write(json.dumps(dictodump, indent='\t')) #sort_keys=True)
    outfile.close()


jsondump(pie_pivot, join(dirname(D.filepath), 'pie_pivot.json') )
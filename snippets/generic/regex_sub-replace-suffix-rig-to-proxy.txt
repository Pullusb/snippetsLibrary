# replace rig suffix (eg:sauce.rig) by '_proxy'  (eg:sauce_proxy). with ignorecase
name = re.sub(r'[\._-]+rigs?$', '_proxy', 'rig_sauce.rig', flags=re.I)
print("name", name)#Dbg

# possible end flag, One or more letters from the set 'I', 'L', 'M', 'S', 'U', 'X'.
# re.I (ignore case)
# re.L (locale dependent)
# re.M (multi-line)
# re.S (dot matches all)
# re.U (Unicode dependent)
# re.X (verbose)

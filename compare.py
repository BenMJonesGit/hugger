# python compare.py dockerName
#
#   If 'dockerName.cmp' exists in the "cmp" folder, read its lines into currSet.
#   Do a 'docker diff dockerName'.  Store the result in 'dockerName.cmp'.  Then
#   check each line to see if it already exists in set.  If not, add it
#   to diffSet.  Create a new 'dockerName.cmp' from this result.  Print out
#   diffset.
#
#   Note that "dockerName" is assigned automatically when a docker container
#   is run.  Or you can specify your own "dockerName" using the --name argument.

import sys
import os

z = len(sys.argv)
if z < 2:
    exit
    
name = sys.argv[1]
currSet = set()
diffSet = set()

# Read in the last diff file:
try:
    file = open(f"cmp/{name}.cmp")
    for line in file:
        currSet.add(line)
            
    file.close()
       
except:
    pass

# Now do a 'docker diff name' and pipe the result to 'name.txt':
os.system(f"docker diff {name} > cmp/{name}.cmp")

# Now read in the new 'name.txt' and generate difference set:
try:
    file = open(f"cmp/{name}.cmp")
    for line in file:
        if line not in currSet:
            diffSet.add(line)
            
    file.close()
    
    diffs = sorted(diffSet)
    for line in diffs:
        print(line.rstrip())
except:
    print(f"New cmp/{name}.cmp not found")

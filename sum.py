#!/usr/bin/python

#------------------------------------------
# Unix sum script: Maintained by Dan Fowler
# Website: dsfcode.com
# Version 1.0.0
#------------------------------------------

import sys
import argparse

# Parse the args
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--groupBy", action="store", help="Group by columns", dest="groupBy")
parser.add_argument("-s", "--sum", action="store", help="Sum columns", dest="sum")
parser.add_argument("-f", "--field", action="store", help="Fields to be printed", dest="field")
parser.add_argument("-c", "--char", action="store", default="\t", help="Input field delimiter", dest="char")
args = vars(parser.parse_args())

# Create int args lists
if args['sum'] == None:
	sum = None
else:
	sum = [ int(s) for s in args['sum'].split(',') ]
if args['groupBy'] == None:
	groupBy = None
else:
	groupBy = [ int(g) for g in args['groupBy'].split(',') ]
if args['field'] == None:
	field = None
else:
	field = [ int(f) for f in args['field'].split(',') ]

# Create print function
def printData(l):
	if field == None:
		print args['char'].join(str(x) for x in l)
	else:
		print args['char'].join(str(l[x-1]) for x in field)

# Create int casting function for summed output
def sumInts(l):
	if sum != None:
		for s in sum:
			if int(l[s-1]) == l[s-1]:
				l[s-1] = int(l[s-1])

# Initialize first row var
first_row = True

# Loop through stdin
for row in sys.stdin:
	# Read the entire row into a list
	row_list = list(row.strip().split(args['char']))
	# Cast summing columns as floats
	if sum != None:
		for s in sum:
			row_list[s-1] = float(row_list[s-1])
	# Create the sum groupBy key
	if groupBy != None:
		key = [ row_list[g-1] for g in groupBy ]
	else:
		key = None

	# Initialize first row vars
	if first_row:
		last_row = row_list
		last_key = key
		first_row = False
	else:
		# Keep summing if keys are equal
		if key == last_key:
			if sum != None:
				for s in sum:
					row_list[s-1] = row_list[s-1] + last_row[s-1]
			# Reset keys
			last_row = row_list
			last_key = key
			# Print out cols if only -f is used
			if key == None and sum == None:
				printData(last_row)
		else:
			# Remove .0 from ints
			sumInts(last_row)
			# Output Data
			printData(last_row)
			# Reset keys
			last_row = row_list
			last_key = key

# Remove .0 from ints
sumInts(row_list)
# Print final row
printData(row_list)


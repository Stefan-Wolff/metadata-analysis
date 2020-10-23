#!/usr/bin/env python
#

					
def run(data):
	count = 0
	all = set()
	
	for record in data:
		hash = record["title"].lower() + "#" + str(record["publication_year"])
		if hash in all:
			count += 1
		else:
			all.add(hash)

			
	return (count, len(data))


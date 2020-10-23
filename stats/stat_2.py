#!/usr/bin/env python
#

					
def run(data):
	duplicates = 0
	all = set()
	for record in data:
		year = record["publication_year"]
		if year in all:
			duplicates += 1
		else:
			all.add(year)

	return (duplicates, len(data))
			

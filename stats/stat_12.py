#!/usr/bin/env python
#

					
def run(data):
	author_sets = {}
	count = 0
		
	for record in data:
		author_num = len(record["authors"]["authors"])
		title = record["title"]

		author_sets.setdefault(title, [])
					
		if author_num in author_sets[title]:
			count += 1
		else:
			author_sets[title].append(author_num)
			
			
	return (count, len(data))

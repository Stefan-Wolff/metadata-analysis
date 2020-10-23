#!/usr/bin/env python
#

					
def run(data):
	title_duplicates = 0
	all_titles = set()
	for record in data:
		title = record["title"].lower()
		if title in all_titles:
			title_duplicates += 1
		else:
			all_titles.add(title)

			
	return (title_duplicates, len(data))


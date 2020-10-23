#!/usr/bin/env python
#

					
def run(data):
	title_duplicates = 0
	
	first_titles = {}
	dupls = {}
	
	all_titles = set()
	for record in data:
		title = record["title"].lower()
		if title in all_titles:
			title_duplicates += 1
			
			dupls.setdefault(title, [ first_titles[title] ])
			dupls[title].append(record["doi"])
		else:
			all_titles.add(title)
			first_titles[title] = record["doi"]

	print(dupls.values())
			
	return (title_duplicates, len(data))


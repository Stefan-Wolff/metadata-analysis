#!/usr/bin/env python
#
					

def containsSet(allSets, searchSet):
	for current in allSets:
		if current == searchSet:
			return True
			
	return False

					
def run(data):
	author_sets = {}
	count = 0
		
	for record in data:
		authors = record["authors"]["authors"]
		title = record["title"]
		current_set = set()
		for author in authors:
			id = author["id"]
			current_set.add(id)

		author_sets.setdefault(title, [])
					
		if containsSet(author_sets[title], current_set):
			count += 1
		else:
			author_sets[title].append(current_set)


	return (count, len(data))

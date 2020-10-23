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
		current_set = set()
		id_hash = 0
		for author in authors:
			id = author["id"]
			current_set.add(id)
			id_hash += id
					
		author_sets.setdefault(id_hash, [])
					
		if containsSet(author_sets[id_hash], current_set):
			count += 1
		else:
			author_sets[id_hash].append(current_set)
			
	return (count, len(data))

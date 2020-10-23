#!/usr/bin/env python
#

from . import lib


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
		name_hash = 0
		for author in authors:
			short_name = lib.buildShortName(author["full_name"])
			current_set.add(short_name)
			name_hash += hash(short_name)
					
		author_sets.setdefault(name_hash, [])
					
		if containsSet(author_sets[name_hash], current_set):
			count += 1
		else:
			author_sets[name_hash].append(current_set)
			
	return (count, len(data))

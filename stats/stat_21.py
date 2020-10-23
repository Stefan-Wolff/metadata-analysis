#!/usr/bin/env python
#
					
import re
import logging					


def run(data):
	authors = {}
	for record in data:
		for author in record["authors"]["authors"]:
			authors[author["id"]] = author["full_name"].split(" ")[-1].lower()

	count = 0
	author_names = {}
	
	for name in authors.values():
		if name in author_names:
			author_names[name] += 1
			count += 1
		else:
			author_names[name] = 1
			

	logging.info("\t top 500:")
	i = 0
	for name, num in sorted(author_names.items(), key=lambda x: x[1], reverse=True): 					# desc sorted by value
		if 1 < num:
			logging.info("\t\t " + name.title() + ": " + str(num))
			i += 1
			if 500 == i:
				break
			
			
			
	return (count, len(authors))

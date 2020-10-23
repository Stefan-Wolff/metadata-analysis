#!/usr/bin/env python
#
					
from . import lib
import logging					


def run(data):
	authors = {}
	for record in data:
		for author in record["authors"]["authors"]:
			authors[author["id"]] = lib.buildShortName(author["full_name"])

	count = 0
	author_names = {}
	
	for name in authors.values():
		if name in author_names:
			author_names[name] += 1
			count += 1
		else:
			author_names[name] = 1		
			
			
	return (count, len(authors))

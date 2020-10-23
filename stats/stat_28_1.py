#!/usr/bin/env python
#

import logging
from . import lib


### main
def run(data):
	renamed = {}
	
	for record in data:
		author_ids = []
		for author in record["authors"]["authors"]:
			author_name = lib.buildShortName(author["full_name"])
			author_id = author["id"]
			
			renamed.setdefault(author_id, set())
			renamed[author_id].add(author_name)

	logging.info("\t number of authors: " + str(len(renamed)))

	for id, names in list(renamed.items()):
		if 1 == len(names):
			del renamed[id]


	logging.info("\t " + str(len(renamed)) + " authors published under multiple names: " + str(renamed))
	logging.info("\t analysis 28_1 done")

	return -1, -1


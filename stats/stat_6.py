#!/usr/bin/env python
#

import logging
					
def run(data):
	count = {}
	
	for record in data:
		title_len = len(record["title"])
		count.setdefault(title_len, 0)
		count[title_len] += 1

			
	logging.info("\t\t analysis 6: " + str(count))
			
	return (-1, -1)


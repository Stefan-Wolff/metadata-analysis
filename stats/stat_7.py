#!/usr/bin/env python
#

import logging
					
def run(data):
	count = {}
	
	for record in data:
		abstract_len = len(record["abstract"])
		count.setdefault(abstract_len, 0)
		count[abstract_len] += 1

			
	logging.info("\t\t analysis 7: " + str(count))
			
	return (-1, -1)


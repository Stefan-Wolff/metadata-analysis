#!/usr/bin/env python
#

import logging


def run(data):
	author_num = {}
	
	for record in data:
		num = len(record["authors"]["authors"])
		
		author_num.setdefault(num, 0)
		author_num[num] += 1
		

	record_num = len(data)
	for num in sorted(author_num):
		percent = round(100 * author_num[num] / record_num, 4)
		logging.info("\t " + str(num) + " authors: " + str(percent) + " % (" + str(author_num[num]) + " / " + str(record_num) + ")")


	return (-1, -1)

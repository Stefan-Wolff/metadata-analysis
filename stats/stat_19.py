#!/usr/bin/env python
#
# requires: pip install edlib

import edlib
import logging
import multiprocessing
import sys



def levenshtein(value1, value2, max):
	lev_align = edlib.align(value1, value2, k=max)
	
	return lev_align["editDistance"]


def addMatches(dict_items, start, base_value, max_dist_percent, count):
	base_len = len(base_value)
	max_char_dist = int(max_dist_percent * base_len / 100)

	if 0 == max_char_dist:
		return

	len_start = base_len - max_char_dist
	len_end = base_len + max_char_dist
	
	i = 0
	for value_len, value_set in dict_items:
		if value_len >= len_start and value_len <= len_end:
			for value in value_set:
				if i > start:
					dist = levenshtein(base_value, value, max_char_dist)
					if dist > -1 and dist <= max_char_dist:
						dist_percent = int(100 * dist / base_len)
						count.setdefault(dist_percent, 0)
						count[dist_percent] += 1
				i += 1
		else:
			i += len(value_set)


def run_matching(dict_items, start, end, q, max_dist_percent, thread_id):
	try:
		logging.info("start thread " + str(thread_id) + "  start:" + str(start) + "  end: " + str(end))
		count = {}
		i = 0
		for value_len, value_set in dict_items:
			for value in value_set:
				if i >= start and i < end:
					addMatches(dict_items, i, value, max_dist_percent, count)
					if 0 == (i % 1000):
						logging.info("\t analysis 19 progress thread " + str(thread_id) + ": " + str(i) + " - " + str(count))
				i += 1


		q.put(count)
		logging.info("\t analysis 19 thread " + str(thread_id) + " done")
		
	except:
		logging.exception(sys.exc_info()[0])


def run(data):
	len_dict = {}
	max_dist_percent = 30
		
	for record in data:
		value = record["title"].lower()
		value_len = len(value)
		
		len_dict.setdefault(value_len, [])
		len_dict[value_len].append(value)


	thread_num = int(multiprocessing.cpu_count() / 2)
	step_size = int(len(data) / thread_num)
	dict_items = len_dict.items()
	procs = []
	q = multiprocessing.Queue()
	
	for i in range(0, thread_num):
		start = i * step_size
		end = (i+1) * step_size if (i < thread_num-1) else len(data)
		p = multiprocessing.Process(target=run_matching, args=(dict_items, start, end, q, max_dist_percent, i, ))
		p.start()
		procs.append(p)


	for p in procs:
		p.join()


	count = {}
	while not q.empty():
		sub_count = q.get()
		for dist, num in sub_count.items():
			count.setdefault(dist, 0)
			count[dist] += num
		
	
	logging.info("\t\t analysis 19: " + str(count))


	return -1, -1


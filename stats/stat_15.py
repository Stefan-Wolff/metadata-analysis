#!/usr/bin/env python
#
# requires: pip install edlib

import edlib
import logging
from . import lib



def levenshtein(value1, value2, max):
	lev_align = edlib.align(value1, value2, k=max)
	
	return lev_align["editDistance"]


def run(data):
	len_dict = {}
	max_dist_percent = 10
		
	sorted = {}
		
	for record in data:
		key = str(record["publication_year"])
		for author in record["authors"]["authors"]:
			key += "#" + lib.buildShortName(author["full_name"])
		
		sorted.setdefault(key, [])
		sorted[key].append(record["title"].lower())

	count = 0

	for titles in sorted.values():
		i = 0
		for title in titles:
			j = 0
			title_len = len(title)
			for title2 in titles:
				if i < j:
					max_char_dist = int(max_dist_percent * title_len / 100)
					if max_char_dist >= abs(len(title2) - title_len):
						dist = levenshtein(title, title2, max_char_dist)
						if dist > -1 and dist <= max_char_dist:
							count += 1
				j += 1
			i += 1


	return (count, len(data))


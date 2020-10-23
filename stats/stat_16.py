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
	max_dist_percent = 5
	max_dist_percent2 = 2
		
	sorted = {}
		
	for record in data:
		key = str(record["publication_year"])
		for author in record["authors"]["authors"]:
			key += "#" + lib.buildShortName(author["full_name"])
		
		sorted.setdefault(key, [])
		sorted[key].append([record["title"].lower(), record["abstract"].lower()])

	count = 0

	for entries in sorted.values():
		i = 0
		for entry in entries:
			title = entry[0]
			abstract = entry[1]
			title_len = len(title)
			abstract_len = len(abstract)
			
			j = 0
			for entry2 in entries:
				if i < j:
					title2 = entry2[0]
					abstract2 = entry2[1]
					max_char_dist = int(max_dist_percent * title_len / 100)
					if max_char_dist >= abs(len(title2) - title_len):
						dist = levenshtein(title, title2, max_char_dist)
						if dist > -1 and dist <= max_char_dist:
							max_char_dist2 = int(max_dist_percent2 * abstract_len / 100)
							if max_char_dist2 >= abs(len(abstract2) - abstract_len):
								dist2 = levenshtein(abstract, abstract2, max_char_dist2)
								if dist2 > -1 and dist2 <= max_char_dist2:
									count += 1
				j += 1
			i += 1


	return (count, len(data))


#!/usr/bin/env python
#

import os
import logging
import csv
from . import lib


MIN_AUTHORS = 2
MAX_AUTHORS = 10


csv.register_dialect('default', delimiter	= ',',
								quoting		= csv.QUOTE_MINIMAL)


### functions
def writeCSV(fileName, count):
	with open(fileName, 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=["level", "group_size", "count", "count_all", "count_percent"], dialect='default')
		writer.writeheader()
		
		for level, level_counts in count.items():
			for group_size, counts in level_counts.items():
				count_percent = round(100 * counts[0]/counts[1],3) if (0 != counts[1]) else 0
				writer.writerow({"level": level, "group_size": group_size, "count": counts[0], "count_all": counts[1], "count_percent": count_percent})


# returns True if group containing min one namesake		
def contains_namesake(names, namesakes, name_doi_id, dois, level):
	found_namesakes = 0
	for name in names:
		if name in namesakes:		
			cur_doi_id = name_doi_id[name]
			author_id = cur_doi_id[dois[0]]
			
			for i in range(1, level):
				next_id = cur_doi_id[dois[i]]
				if author_id != next_id:
					found_namesakes += 1
					if 1 < found_namesakes:
						return False
					
					
	return 1 == found_namesakes


def group_permutation(group, cur_group, member_i, result):
	for i in range(member_i+1, len(group)):
		new_group = list(cur_group)
		new_group.append(group[i])
		if MIN_AUTHORS <= len(new_group):
			result.append(new_group)
		group_permutation(group, new_group, i, result)


def run_comparison(doi_names, name_doi_id, namesakes):
	i = 0
	groups = {}
	for doi, group in doi_names.items():							# collect all author groups
		perm_groups = []
		group_permutation(sorted(group), [], -1, perm_groups)
		for perm_group in perm_groups:
			group_hash = "#".join(perm_group)
			groups.setdefault(group_hash, [perm_group, []])
			groups[group_hash][1].append(doi)
			
		i += 1
		if 0 == (i % 1000):
			logging.info("\t analysis 31 group progress: " + str(i))

	logging.info("\t found author groups: " + str(len(groups)))

	count = {}
	for group_hash, group_info in groups.items():					# log sizes of found author groups
		names = group_info[0]
		group_size = len(names)
		dois = group_info[1]
		level = len(dois)
		if 1 < level:
			count.setdefault(level, {})
			count[level].setdefault(group_size, [0, 0])
			count[level][group_size][1] += 1
			if contains_namesake(names, namesakes, name_doi_id, dois, level):
				count[level][group_size][0] += 1


	logging.info("\t analysis 31 done: " + str(count))

	return count


### main
def run(data):
	# init data structure
	doi_names = {}
	name_doi_id = {}
	name_id = {}
	namesakes = set()
	for record in data:
		author_num = len(record["authors"]["authors"])
		if MIN_AUTHORS > author_num or MAX_AUTHORS < author_num:
			continue

		doi = record["doi"]

		publ_authors = set()
		for author in record["authors"]["authors"]:
			name = author["full_name"]
			
			if name in name_id and author["id"] != name_id[name]:
				namesakes.add(name)
			else:
				name_id[name] = author["id"]
			
			publ_authors.add(name)
			name_doi_id.setdefault(name, {})
			
			if doi in name_doi_id[name]:
				name_doi_id[name][doi] = doi		# if two authors of same publication does have the same shortname, then save a author id unique to this publication (then this author will identified as namesake, but not as same person)
			else:
				name_doi_id[name][doi] = author["id"]

		doi_names[doi] = publ_authors




	# run
	count = run_comparison(doi_names, name_doi_id, namesakes)

	# write results
	out_path = os.path.join(os.path.dirname(__file__), '../logs/stats_31.csv')
	writeCSV(out_path, count)


	logging.info("\t analysis 31 done")

	return -1, -1


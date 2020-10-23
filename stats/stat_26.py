#!/usr/bin/env python
#

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
		writer = csv.DictWriter(csvfile, fieldnames=["level", "group_size", "count"], dialect='default')
		writer.writeheader()
		
		for level, level_counts in count.items():
			for group_size, author_count in level_counts.items():
				writer.writerow({"level": level, "group_size": group_size, "count": author_count})


# returns True if group containing min one namesake		
def contains_namesake(names, namesakes, name_doi_id, dois, level):
	for name in names:
		if name in namesakes:		
			cur_doi_id = name_doi_id[name]
			author_id = cur_doi_id[dois[0]]
			
			for i in range(1, level):
				next_id = cur_doi_id[dois[i]]
				if author_id != next_id:
					return True
					
					
	return False


def group_permutation(group, cur_group, member_i, result):
	member_in_base_group = True if cur_group else False

	for i in range(member_i+1, len(group)):
		new_group = list(cur_group)
		new_group.append(group[i])
		if member_in_base_group:
			result.append(new_group)
		group_permutation(group, new_group, i, result)


def run_comparison(doi_names):
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
			logging.info("\t analysis 26 group progress: " + str(i))

	logging.info("\t found author groups: " + str(len(groups)))

	i = 0
	count = {}
	for group_hash, group_info in groups.items():					# log sizes of found author groups
		names = group_info[0]
		group_size = len(names)
		dois = group_info[1]
		level = len(dois)
		if 1 < level and MIN_AUTHORS <= group_size:
			count.setdefault(level, {})
			count[level].setdefault(group_size, 0)
			count[level][group_size] += 1

		i += 1
		if 0 == (i % 1000):
			logging.info("\t analysis 26 progress thread: " + str(i))


	logging.info("\t analysis 26 done: " + str(count))

	return count


### main
def run(data):
	# init data structure
	doi_authors = {}
	for record in data:
		author_num = len(record["authors"]["authors"])
		if MIN_AUTHORS > author_num or MAX_AUTHORS < author_num:
			continue

		doi = record["doi"]
		publ_authors = set()
		for author in record["authors"]["authors"]:
			publ_authors.add(lib.buildShortName(author["full_name"]))

		doi_authors[doi] = publ_authors

	# run
	count = run_comparison(doi_authors)

	# write results
	writeCSV("stats_26.csv", count)


	logging.info("\t analysis 26 done")

	return -1, -1


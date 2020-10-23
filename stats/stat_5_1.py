#!/usr/bin/env python
#


def run(data):
	count = 0
	all_abstracts = set()
	first = {}
	dupls = {}
	for record in data:
		abstract = record["abstract"].lower()
		if abstract in all_abstracts:
			count += 1
			dupls[abstract] = [ first[abstract], record["doi"] ]
		else:
			all_abstracts.add(abstract)
			first[abstract] = record["doi"]

	print(dupls.values())
			
	return (count, len(data))

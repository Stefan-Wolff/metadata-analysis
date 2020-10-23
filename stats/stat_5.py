#!/usr/bin/env python
#


def run(data):
	count = 0
	all_abstracts = set()
	for record in data:
		abstract = record["abstract"].lower()
		if abstract in all_abstracts:
			count += 1
		else:
			all_abstracts.add(abstract)

	return (count, len(data))

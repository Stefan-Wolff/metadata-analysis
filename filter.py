#!/usr/bin/env python
#

import os
import logging
import sys
import json
import re
from stats import lib
from os import listdir
from os.path import isfile, join


IN_PATH = 'raw-data'
OUT_FILE = 'data/ieee_filtered.json'


logging.basicConfig(format		=	"%(asctime)s %(levelname)s: %(message)s", 
					filename	=	'logs/filter.log',
					level		=	logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())


TITLES_EXCLUDED = [
	"authors' reply",
	"foreword",
	"call for papers",
	"guest editorial",
	"editorial",
	"eic editorial",
	"scanning the issue",
	"editor's note",
	"a message from the new editor-in-chief",
	"section meetings",
	"changes in the editorial board",
	"new associate editors",
	"introduction of new associate editors",
	"editorial conference comments by the general chair",
	"foreword to the special issue on hyperspectral image and signal processing" ]
	

class RecordIterator:

	def __init__(self, data_dir):
		self.data_dir = data_dir
	
	def __iter__(self):
		self.data_files = [f for f in listdir(self.data_dir) if isfile(join(self.data_dir, f)) and f.endswith(".json")]
		self.buffer = []
		return self
		
		
	def loadNext(self):
		if 0 == len(self.data_files):
			return False

		filename = self.data_files.pop(0)
		with open(join(self.data_dir, filename)) as file:
			data = json.load(file)
			self.buffer.extend(data)
			
		return 0 != len(data)


	def __next__(self):
		if 0 == len(self.buffer):
			if not self.loadNext():
				raise StopIteration

		return self.buffer.pop(0)
		

### functions

def getPageNumber(value):
	result = value
	if not value.isdigit():
		matches = re.search(r'\d+', result)
		if not matches:
			return None
		result = matches.group()
	
	return int(result)
	
	
def filterByPageNumber(record):
	if not "start_page" in record or not "end_page" in record:
		return False
	else:
		start_page = getPageNumber(record["start_page"])
		end_page = getPageNumber(record["end_page"])
		
		if start_page and end_page:
			return 1 < (end_page - start_page)
		else:
			return False


def validate(record):
	for field in ["doi", "title", "abstract"]:
		if not field in record or "" == record[field]:
			return False
		
	if 1990 > record["publication_year"]:
		return False

	if not filterByPageNumber(record):
		return False
			
	if 120 > len(record["abstract"]):
		return False
			
	authors = record["authors"]["authors"]
	for author in authors:
		if not "id" in author:
			return False
		
	return 0 != len(authors)


def buildHashes(record):
	result = set()
	hash_1 = record["title"].lower()
	
	for author in record["authors"]["authors"]:
		hash_1 += "#" + str(author["id"])
			
	result.add(hash_1 + "#" + str(record["publication_year"] - 1))
	result.add(hash_1 + "#" + str(record["publication_year"]))
	result.add(hash_1 + "#" + str(record["publication_year"] + 1))
		
		
	hash_2 = record["title"].lower()
	
	for author in record["authors"]["authors"]:
		hash_2 += "#" + lib.buildShortName(author["full_name"])
		
	result.add(hash_2 + "#" + str(record["publication_year"] - 1))
	result.add(hash_2 + "#" + str(record["publication_year"]))
	result.add(hash_2 + "#" + str(record["publication_year"] + 1))
	
	
	result.add(record["abstract"].lower())
		
	return result
		

### main
def run():
	result = []
	ids = set()
	hashes = set()
	authors = set()
	total = 0
	for record in iter(RecordIterator(IN_PATH)):
		total += 1
		if not validate(record):
			continue
		if record["doi"] in ids:
			continue
			
		record_hashes = buildHashes(record)		
		if not record_hashes.isdisjoint(hashes):
			continue
		
		for author in record["authors"]["authors"]:
			authors.add(author["id"])
		
		ids.add(record["doi"])
		hashes.update(record_hashes)
		result.append(record)


	with open(OUT_FILE, 'w') as file:
		json.dump(result, file)
	
	logging.info("publication records: " + str(total) + " -> " + str(len(result)) + " records")
	logging.info("author records: " + str(len(authors)))


if "__main__" == __name__:
	run()



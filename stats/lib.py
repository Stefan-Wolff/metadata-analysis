#!/usr/bin/env python
#

import re

def buildShortName(name):
	result = name.lower()
	
	if "," in result:
		commaParts = result.split(",")
		commaParts = reversed(commaParts)
		result = " ".join(result)
	
	result = re.sub(r"[.,-/]", " ", result)
	result = re.sub(r"[ ]+", " ", result)
	result = result.strip()
	
	result = result.replace("ä", "ae")
	result = result.replace("ö", "oe")
	result = result.replace("ü", "ue")
	result = result.replace("ß", "ss")
	
	spaceParts = result.split(" ")
	if 1 < len(spaceParts):
		result = spaceParts[0][0] + " " + spaceParts[-1]
		
	return result
	
